const fs = require('fs');

// Feishu API base
const FEISHU_API = 'https://open.feishu.cn/open-apis';

// Feishu credentials from config
const FEISHU_APP_ID = 'cli_a92780ca08b89bb6';
const FEISHU_APP_SECRET = '6gzhCcNYlHc7vOnGCCdvpbik27O85uz0';

// Get tenant access token
async function getTenantAccessToken() {
    const res = await fetch(`${FEISHU_API}/auth/v3/tenant_access_token/internal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ app_id: FEISHU_APP_ID, app_secret: FEISHU_APP_SECRET })
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
    if (data.code !== 0) throw new Error(`Add Record Failed: ${data.msg} | Fields: ${JSON.stringify(fields)}`);
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
    
    // Find "热点雷达" or "热点追踪" table
    let hotTable = tables.find(t => t.name.includes('热点'));
    if (!hotTable) {
        console.error('\n⚠️ No "热点" table found. Using first table.');
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
    
    // Calculate expiry timestamp (14 days from now) - Feishu uses milliseconds
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 14);
    const expiryTimestamp = expiryDate.getTime(); // Unix timestamp in milliseconds
    
    // Add records
    console.log('\n📝 Adding hot topic records...\n');
    let successCount = 0;
    let failCount = 0;
    
    for (const article of hotData.articles.slice(0, 10)) {
        // Build record fields
        const fields = {
            "热点标题": article.title,
            "来源": article.source,
            "相关度": article.relevance_score >= 80 ? "高" : article.relevance_score >= 60 ? "中" : "低",
            "选题建议": article.topic_suggestion,
            "原文链接": article.url,
            "过期时间": expiryTimestamp,
            "热度排名": article.rank,
            "状态": "待处理"
        };
        
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
    console.log(`   📍 Table URL: https://ai-zhineng.feishu.cn/base/${appToken}`);
    
    return { successCount, failCount };
}

main().catch(e => {
    console.error(`\n❌ Fatal error: ${e.message}`);
    console.error(e.stack);
    process.exit(1);
});
