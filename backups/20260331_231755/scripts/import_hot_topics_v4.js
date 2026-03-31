const fs = require('fs');

// Feishu API base
const FEISHU_API = 'https://open.feishu.cn/open-apis';

// Feishu credentials
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
    if (data.code !== 0) throw new Error(`Add Record Failed: ${data.msg}`);
    return data.data.record;
}

// Main function
async function main() {
    const appToken = 'Xb0abYaXlayTnNsU2Oocrp42nUh';
    
    // Load hot topics data
    const dataPath = '/root/.openclaw/workspace/memory/hot_topics_2026-03-12.json';
    const hotData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    
    console.log(`📊 Loaded ${hotData.articles.length} hot topics\n`);
    
    // List tables
    console.log(`🔍 Listing tables for Base...`);
    const tables = await listTables(appToken);
    tables.forEach(t => console.log(`  - ${t.name}`));
    
    const hotTable = tables.find(t => t.name.includes('热点')) || tables[0];
    const tableId = hotTable.table_id;
    console.log(`\n✅ Using table: ${hotTable.name}\n`);
    
    // Get table fields to understand field types
    const schemaUrl = `${FEISHU_API}/bitable/v1/apps/${appToken}/tables/${tableId}/fields`;
    const schemaData = await apiRequest(schemaUrl);
    
    let urlFieldName = '原文链接';
    let dateFieldName = '过期时间';
    
    if (schemaData.code === 0) {
        const urlField = schemaData.data.items.find(f => f.field_name.includes('链接') || f.field_name.includes('URL'));
        const dateField = schemaData.data.items.find(f => f.field_name.includes('时间') || f.field_name.includes('日期'));
        if (urlField) urlFieldName = urlField.field_name;
        if (dateField) dateFieldName = dateField.field_name;
        console.log('Fields:', schemaData.data.items.map(f => `${f.field_name}(${f.field_type})`).join(', '));
    }
    
    // Calculate expiry timestamp
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 14);
    const expiryTimestamp = expiryDate.getTime();
    
    // Add records
    console.log('\n📝 Adding hot topic records...\n');
    let successCount = 0;
    let failCount = 0;
    
    for (const article of hotData.articles.slice(0, 10)) {
        // Build record fields - skip URL field if it causes issues
        const fields = {
            "热点标题": article.title,
            "来源": article.source,
            "相关度": article.relevance_score >= 80 ? "高" : article.relevance_score >= 60 ? "中" : "低",
            "选题建议": article.topic_suggestion,
            "过期时间": expiryTimestamp,
            "热度排名": article.rank,
            "状态": "待处理"
        };
        
        // Only add URL if it's a valid http(s) URL and not too long
        if (article.url && article.url.length < 1000 && article.url.startsWith('http')) {
            try {
                // Truncate URL if needed
                fields[urlFieldName] = article.url.substring(0, 500);
            } catch(e) {
                // Skip URL if problematic
            }
        }
        
        try {
            const record = await addRecord(appToken, tableId, fields);
            console.log(`✅ [${article.rank}] ${article.title.substring(0, 40)}... (相关度: ${article.relevance_score})`);
            successCount++;
        } catch (e) {
            console.error(`❌ [${article.rank}] Failed: ${e.message.substring(0, 100)}`);
            failCount++;
        }
        
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(`\n📊 Summary:`);
    console.log(`   ✅ Success: ${successCount}`);
    console.log(`   ❌ Failed: ${failCount}`);
    console.log(`   📍 Table: https://ai-zhineng.feishu.cn/base/${appToken}`);
}

main().catch(e => {
    console.error(`\n❌ Fatal error: ${e.message}`);
    process.exit(1);
});
