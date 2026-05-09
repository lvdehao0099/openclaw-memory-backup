const fs = require('fs');

// Feishu API base
const FEISHU_API = 'https://open.feishu.cn/open-apis';

// Get tenant access token
async function getTenantAccessToken() {
    const appId = process.env.FEISHU_APP_ID;
    const appSecret = process.env.FEISHU_APP_SECRET;
    
    if (!appId || !appSecret) {
        throw new Error('Missing FEISHU_APP_ID or FEISHU_APP_SECRET environment variables');
    }
    
    const res = await fetch(`${FEISHU_API}/auth/v3/tenant_access_token/internal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ app_id: appId, app_secret: appSecret })
    });
    
    const data = await res.json();
    if (data.code !== 0) throw new Error(`Auth failed: ${data.msg}`);
    return data.tenant_access_token;
}

// API request helper
async function apiRequest(url, method = 'GET', body = null) {
    const token = await getTenantAccessToken();
    const options = {
        method,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    };
    if (body) options.body = JSON.stringify(body);

    const res = await fetch(url, options);
    const data = await res.json();
    return data;
}

// List tables in a base
async function listTables(appToken) {
    const url = `${FEISHU_API}/bitable/v1/apps/${appToken}/tables`;
    const data = await apiRequest(url);
    if (data.code !== 0) throw new Error(`List Tables Failed: ${data.msg}`);
    return data.data.items;
}

// Add record to table
async function addRecord(appToken, tableId, fields) {
    const url = `${FEISHU_API}/bitable/v1/apps/${appToken}/tables/${tableId}/records`;
    const data = await apiRequest(url, 'POST', { fields });
    if (data.code !== 0) throw new Error(`Add Record Failed: ${data.msg}`);
    return data.data.record;
}

// Main function
async function main() {
    // Base token from URL: https://ai-zhineng.feishu.cn/base/Xb0abYaXlayTnNsU2Oocrp42nUh
    const appToken = 'Xb0abYaXlayTnNsU2Oocrp42nUh';
    
    // Load hot topics data
    const dataPath = '/root/.openclaw/workspace/memory/hot_topics_2026-03-12.json';
    const hotData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    
    console.log(`📊 Loaded ${hotData.articles.length} hot topics\n`);
    
    // List tables
    console.log(`🔍 Listing tables for Base...`);
    const tables = await listTables(appToken);
    console.log(`Found ${tables.length} tables:`);
    tables.forEach(t => console.log(`  - ${t.name} (ID: ${t.table_id})`));
    
    // Find "热点雷达" table
    let hotTable = tables.find(t => t.name.includes('热点') || t.name.includes('雷达'));
    if (!hotTable) {
        hotTable = tables.find(t => t.name.includes('追踪'));
    }
    if (!hotTable) {
        console.error('\n⚠️ No "热点雷达" table found. Using first table.');
        if (tables.length === 0) {
            console.error('❌ No tables available!');
            process.exit(1);
        }
        hotTable = tables[0];
    }
    
    const tableId = hotTable.table_id;
    console.log(`\n✅ Using table: ${hotTable.name} (ID: ${tableId})\n`);
    
    // Get table fields
    console.log('📋 Getting table schema...');
    const schemaUrl = `${FEISHU_API}/bitable/v1/apps/${appToken}/tables/${tableId}/fields`;
    const schemaData = await apiRequest(schemaUrl);
    let fieldNames = [];
    if (schemaData.code === 0) {
        fieldNames = schemaData.data.items.map(f => f.field_name);
        console.log('Table fields:', fieldNames.join(', '));
    }
    
    // Add records
    console.log('\n📝 Adding hot topic records...\n');
    let successCount = 0;
    let failCount = 0;
    
    for (const article of hotData.articles.slice(0, 10)) {
        // Calculate expiry date (14 days from now)
        const expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + 14);
        const expiryStr = expiryDate.toISOString().split('T')[0];
        
        // Build record fields dynamically based on available fields
        const fields = {};
        
        if (fieldNames.includes('热点标题') || fieldNames.includes('标题')) {
            fields[fieldNames.includes('热点标题') ? '热点标题' : '标题'] = article.title;
        }
        if (fieldNames.includes('来源')) fields['来源'] = article.source;
        if (fieldNames.includes('分类')) fields['分类'] = article.category;
        if (fieldNames.includes('相关度评分')) fields['相关度评分'] = article.relevance_score;
        if (fieldNames.includes('相关度')) {
            fields['相关度'] = article.relevance_score >= 80 ? "高" : article.relevance_score >= 60 ? "中" : "低";
        }
        if (fieldNames.includes('选题建议')) fields['选题建议'] = article.topic_suggestion;
        if (fieldNames.includes('摘要')) fields['摘要'] = article.summary;
        if (fieldNames.includes('链接')) fields['链接'] = article.url;
        if (fieldNames.includes('采集日期')) fields['采集日期'] = hotData.collection_date;
        if (fieldNames.includes('过期时间')) fields['过期时间'] = expiryStr;
        if (fieldNames.includes('排名')) fields['排名'] = article.rank;
        
        // Fallback: try common field names
        if (Object.keys(fields).length === 0) {
            fields['标题'] = article.title;
            fields['内容'] = article.summary;
            fields['日期'] = hotData.collection_date;
        }
        
        try {
            const record = await addRecord(appToken, tableId, fields);
            console.log(`✅ [${article.rank}] ${article.title.substring(0, 40)}... (相关度: ${article.relevance_score})`);
            successCount++;
        } catch (e) {
            console.error(`❌ [${article.rank}] Failed: ${e.message}`);
            failCount++;
        }
        
        // Small delay
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(`\n📊 Summary:`);
    console.log(`   ✅ Success: ${successCount}`);
    console.log(`   ❌ Failed: ${failCount}`);
}

main().catch(e => {
    console.error(`\n❌ Fatal error: ${e.message}`);
    process.exit(1);
});
