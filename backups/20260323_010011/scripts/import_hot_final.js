const fs = require('fs');

const FEISHU_API = 'https://open.feishu.cn/open-apis';
const FEISHU_APP_ID = 'cli_a92780ca08b89bb6';
const FEISHU_APP_SECRET = '6gzhCcNYlHc7vOnGCCdvpbik27O85uz0';

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
    return await res.json();
}

async function listTables(appToken) {
    const url = `${FEISHU_API}/bitable/v1/apps/${appToken}/tables`;
    const data = await apiRequest(url);
    if (data.code !== 0) throw new Error(`List Tables Failed: ${data.msg}`);
    return data.data.items;
}

async function addRecord(appToken, tableId, fields) {
    const url = `${FEISHU_API}/bitable/v1/apps/${appToken}/tables/${tableId}/records`;
    const data = await apiRequest(url, 'POST', { fields });
    if (data.code !== 0) throw new Error(`Add Record Failed: ${data.msg}`);
    return data.data.record;
}

async function main() {
    const appToken = 'Xb0abYaXlayTnNsU2Oocrp42nUh';
    
    const hotData = JSON.parse(fs.readFileSync('/root/.openclaw/workspace/memory/hot_topics_2026-03-12.json', 'utf8'));
    
    console.log(`📊 Loaded ${hotData.articles.length} hot topics\n`);
    
    const tables = await listTables(appToken);
    const hotTable = tables.find(t => t.name.includes('热点')) || tables[0];
    const tableId = hotTable.table_id;
    console.log(`✅ Using table: ${hotTable.name}\n`);
    
    // Calculate expiry timestamp (14 days from now)
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 14);
    const expiryTimestamp = expiryDate.getTime();
    
    console.log('📝 Adding hot topic records...\n');
    let successCount = 0;
    let failCount = 0;
    
    for (const article of hotData.articles.slice(0, 10)) {
        // Build record fields WITHOUT URL
        const fields = {
            "热点标题": article.title,
            "来源": article.source,
            "相关度": article.relevance_score >= 80 ? "高" : article.relevance_score >= 60 ? "中" : "低",
            "选题建议": article.topic_suggestion,
            "过期时间": expiryTimestamp,
            "热度排名": article.rank,
            "状态": "待处理"
        };
        
        try {
            await addRecord(appToken, tableId, fields);
            console.log(`✅ [${article.rank}] ${article.title.substring(0, 40)}... (相关度: ${article.relevance_score})`);
            successCount++;
        } catch (e) {
            console.error(`❌ [${article.rank}] Failed: ${e.message.substring(0, 80)}`);
            failCount++;
        }
        
        await new Promise(r => setTimeout(r, 300));
    }
    
    console.log(`\n📊 Summary:`);
    console.log(`   ✅ Success: ${successCount}`);
    console.log(`   ❌ Failed: ${failCount}`);
    console.log(`   📍 Table: https://ai-zhineng.feishu.cn/base/${appToken}`);
    
    return { successCount, failCount };
}

main().catch(e => {
    console.error(`\n❌ Fatal error: ${e.message}`);
    process.exit(1);
});
