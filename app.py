from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZTE ONU Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #020617 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --border: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #6366f1;
            --success: #10b981;
            --input-bg: rgba(15, 23, 42, 0.6);
            --highlight: #38bdf8;
            --term-header: #1e293b;
        }

        body.light-mode {
            --bg-gradient: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%);
            --card-bg: rgba(255, 255, 255, 0.8);
            --border: #cbd5e1;
            --text-main: #1e293b;
            --text-muted: #475569;
            --input-bg: #f8fafc;
            --term-header: #e2e8f0;
        }

        body.cute-mode {
            --bg-gradient: linear-gradient(135deg, #fdf2f8 0%, #fbcfe8 100%);
            --card-bg: rgba(255, 255, 255, 0.7);
            --border: #f9a8d4;
            --text-main: #831843;
            --text-muted: #be185d;
            --primary: #db2777;
            --input-bg: #fff0f7;
            --highlight: #ec4899;
            --term-header: #fce7f3;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: 'Inter', sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 40px 20px;
            transition: all 0.3s ease;
        }

        /* FIXED: Theme control alignment */
        .theme-control {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-bottom: 20px;
            margin-right: 0;
        }
        .theme-control label {
            margin: 0 10px 0 0;
            font-size: 14px;
            color: var(--text-muted);
            font-weight: 600;
        }
        .theme-control select {
            padding: 10px 18px;
            border-radius: 10px;
            background: var(--card-bg);
            color: var(--text-main);
            border: 1px solid var(--border);
            cursor: pointer;
            font-size: 14px;
            outline: none;
            transition: all 0.3s ease;
        }
        .theme-control select:hover {
            border-color: var(--primary);
        }
        .theme-control select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
        }

        .wrapper { max-width: 1100px; margin: auto; width: 100%; flex: 1; }
        .title { text-align: center; font-size: 36px; font-weight: 800; margin-bottom: 5px; }
        .title span { background: linear-gradient(to right, #818cf8, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { text-align: center; color: var(--text-muted); font-size: 16px; margin-bottom: 40px; font-weight: 500; }
        .grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 30px; }
        .card { background: var(--card-bg); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: 20px; padding: 32px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .form-group { display: flex; flex-direction: column; }
        .form-group.full { grid-column: 1 / -1; }
        label { margin-bottom: 8px; font-size: 13px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }
        input { width: 100%; padding: 14px 16px; border-radius: 10px; border: 1px solid var(--border); background: var(--input-bg); color: var(--text-main); font-size: 15px; outline: none; transition: all 0.3s ease; }
        input:focus { border-color: var(--primary); }
        .actions { margin-top: 32px; }
        button.generate { width: 100%; padding: 16px 24px; border: none; border-radius: 10px; font-weight: 600; cursor: pointer; background: linear-gradient(135deg, var(--primary), #818cf8); color: white; transition: all 0.3s ease; }
        .output-card { margin-bottom: 30px; background: var(--input-bg); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
        .terminal-header { background: var(--term-header); padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); }
        .terminal-controls { display: flex; gap: 8px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot.red { background: #ef4444; } .dot.yellow { background: #eab308; } .dot.green { background: #22c55e; }
        .terminal-title { font-size: 13px; color: var(--text-muted); }
        .copy-btn { background: rgba(255,255,255,0.05); color: var(--text-main); border: 1px solid var(--border); padding: 6px 14px; border-radius: 6px; cursor: pointer; }
        .copy-btn:hover { background: rgba(255,255,255,0.1); }
        pre { padding: 20px; color: var(--text-main); overflow-x: auto; overflow-y: auto; white-space: pre-wrap; font-family: monospace; font-size: 14px; margin: 0; }
        .input-value { color: var(--highlight); font-weight: 700; background: rgba(56, 189, 248, 0.15); padding: 2px 6px; border-radius: 4px; }
        .footer { text-align: center; margin-top: 40px; color: var(--text-muted); font-size: 14px; padding: 20px; }
        @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>

<div class="wrapper">
    <div class="theme-control">
        <label>Theme:</label>
        <select id="themeSelector" onchange="setTheme(this.value)">
            <option value="">Dark Mode</option>
            <option value="light-mode">Light Mode</option>
            <option value="cute-mode">Cute Mode</option>
        </select>
    </div>
    <div class="title">ZTE ONU <span>Config Generator</span></div>
    <div class="subtitle">YFCI Network Provisioning</div>

    <div class="grid">
        <div class="card">
            <form method="POST">
                <div class="form-grid">
                    <div class="form-group"><label>PPPoE Username</label><input name="user" value="{{ user }}" placeholder="AN1914" required></div>
                    <div class="form-group"><label>PPPoE Password</label><input name="pass" value="{{ password }}" placeholder="rlVjfB2q0F" required></div>
                    <div class="form-group full"><label>Serial Number (SN)</label><input name="sn" value="{{ sn }}" placeholder="ZTEGCED95CA6" required></div>
                    <div class="form-group"><label>ONU Type</label><input name="type" value="{{ onu_type }}" placeholder="F672YV9.1" required></div>
                    <div class="form-group"><label>Frame/Slot/Port</label><input name="port" value="{{ port }}" placeholder="1/3/15" required></div>
                    <div class="form-group"><label>ONU ID</label><input name="onu" value="{{ onu_id }}" placeholder="8" required></div>
                    <div class="form-group"><label>SVLAN</label><input name="svlan" value="{{ svlan }}" placeholder="2502" required></div>
                </div>
                <div class="actions"><button class="generate" type="submit">Generate Configuration</button></div>
            </form>
        </div>

        <div class="card">
            <div class="output-card">
                <div class="terminal-header">
                    <div class="terminal-controls"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
                    <div class="terminal-title">ONU Config Script</div>
                    <button class="copy-btn" type="button" onclick="copyText('configOut', this)">Copy</button>
                </div>
                <pre id="configOut">{{ config_script | safe }}</pre>
            </div>
            <div class="output-card">
                <div class="terminal-header">
                    <div class="terminal-controls"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
                    <div class="terminal-title">ONU Type Add Script</div>
                    <button class="copy-btn" type="button" onclick="copyText('onuTypeOut', this)">Copy</button>
                </div>
                <pre id="onuTypeOut">{{ onu_type_script | safe }}</pre>
            </div>
        </div>
    </div>
</div>

<footer class="footer">Developed for YFCI Team | &copy; Sandy@2026</footer>

<script>
    const fields = ["port", "type", "sn", "onu", "user", "pass", "svlan"];
    window.onload = () => { 
        fields.forEach(f => { const el = document.querySelector(`[name="${f}"]`); const val = localStorage.getItem(f); if(el && val && !el.value) el.value = val; });
        const savedTheme = localStorage.getItem("theme");
        if(savedTheme) { document.body.className = savedTheme; document.getElementById("themeSelector").value = savedTheme; }
    };
    fields.forEach(f => { const el = document.querySelector(`[name="${f}"]`); if(el) el.addEventListener("input", () => localStorage.setItem(f, el.value)); });
    
    function setTheme(theme) { document.body.className = theme; localStorage.setItem("theme", theme); }
    function copyText(id, btn) { const elem = document.getElementById(id); const text = elem.innerText.trim(); if(!text) return; navigator.clipboard.writeText(text); btn.innerText = "Copied!"; setTimeout(() => btn.innerText = "Copy", 2000); }
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    context = {
        "port": "", "onu_type": "", "sn": "", "onu_id": "",
        "user": "", "password": "", "svlan": "",
        "onu_type_script": "", "config_script": ""
    }
    if request.method == "POST":
        context.update({
            "port": request.form.get("port", ""),
            "onu_type": request.form.get("type", ""),
            "sn": request.form.get("sn", ""),
            "onu_id": request.form.get("onu", ""),
            "user": request.form.get("user", ""),
            "password": request.form.get("pass", ""),
            "svlan": request.form.get("svlan", "")
        })
        def highlight(val): return f'<span class="input-value">{val}</span>'
        context["config_script"] = f"""interface gpon_olt-{highlight(context['port'])}
 onu {highlight(context['onu_id'])} type ZXHN-{highlight(context['onu_type'])} sn {highlight(context['sn'])}
 bind-onu {highlight(context['onu_id'])} profile line HSI-Nolimit
 bind-onu {highlight(context['onu_id'])} profile service HSI-Nolimit
$
interface gpon_onu-{highlight(context['port'])}:{highlight(context['onu_id'])}
 name {highlight(context['user'])}
$
interface vport-{highlight(context['port'])}.{highlight(context['onu_id'])}:1
 service-port 1 user-vlan 1000 vlan 11 svlan {highlight(context['svlan'])}
$
pon-onu-mng gpon_onu-{highlight(context['port'])}:{highlight(context['onu_id'])}
 security-mgmt 1 state enable mode forward protocol https
 security-mgmt 2 state enable mode forward protocol telnet
 security-mgmt 3 state enable mode forward protocol web
 wan-ip ipv4 mode pppoe auth pap username {highlight(context['user'])} password {highlight(context['password'])} vlan-profile HSI-VLAN host 1
 wan 1 ethuni 1,2,3,4 ssid 1,5 service internet host 1
$"""
        context["onu_type_script"] = f"""pon
onu-type ZXHN-{highlight(context['onu_type'])} gpon description 4ETH,2POTS,8WIFI max-tcont 8 max-gemport 32 max-iphost 6 max-ipv6-host 6
onu-type-if ZXHN-{context['onu_type']} eth_0/1
onu-type-if ZXHN-{context['onu_type']} eth_0/2
onu-type-if ZXHN-{context['onu_type']} eth_0/3
onu-type-if ZXHN-{context['onu_type']} eth_0/4
onu-type-if ZXHN-{context['onu_type']} pots_0/1
onu-type-if ZXHN-{context['onu_type']} wifi_0/1
onu-type-if ZXHN-{context['onu_type']} wifi_0/2
onu-type-if ZXHN-{context['onu_type']} wifi_0/3
onu-type-if ZXHN-{context['onu_type']} wifi_0/4
onu-type-if ZXHN-{context['onu_type']} wifi_0/5
onu-type-if ZXHN-{context['onu_type']} wifi_0/6
onu-type-if ZXHN-{context['onu_type']} wifi_0/7
onu-type-if ZXHN-{context['onu_type']} wifi_0/8"""
    return render_template_string(HTML_TEMPLATE, **context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
