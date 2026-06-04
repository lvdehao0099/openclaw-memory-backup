# 邮箱配置信息

**收件邮箱：** 75623116@qq.com
**发件邮箱：** m13998517880@163.com（163邮箱，SMTP已配置）
**用途：** 周报、天气提醒、系统通知

---

# 火山引擎即梦AI账号

**账号信息：**
- 用户名：xiami
- 登录密码：maoPI870929
- 登录地址：https://console.volcengine.com/auth/login/user/2102320925
- 所属主账号ID：2102320925
- Access Key ID：AKLTYzQ2YTA0NWMxZjQ5NGZjM2FkODNhNWQ2NGI5ZDcwMmY
- Secret Access Key：T0RNMlpETmtZemhrWlRJek5HWTBZbUkwT0RJNU1qWmxObVprT1RjMVpEUQ==

**配置时间：** 2026-03-09
**用途：** AI生图/生视频，用于公众号配图、产品宣传图

**使用方法：**
```bash
cd ~/.openclaw/workspace/skills/jimeng-ai
export VOLCENGINE_AK="AKLTYzQ2YTA0NWMxZjQ5NGZjM2FkODNhNWQ2NGI5ZDcwMmY"
export VOLCENGINE_SK="T0RNMlpETmtZemhrWlRJek5HWTBZbUkwT0RJNU1qWmxObVprT1RjMVpEUQ=="
npx ts-node scripts/text2image.ts "提示词" --version v31 --ratio 3:4
```
