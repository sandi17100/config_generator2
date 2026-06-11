from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    port = ""
    onu_type = ""
    sn = ""
    onu_id = ""
    user = ""
    password = ""
    svlan = ""

    onu_type_script = ""
    config_script = ""

    if request.method == "POST":
        port = request.form.get("port", "")
        onu_type = request.form.get("type", "")
        sn = request.form.get("sn", "")
        onu_id = request.form.get("onu", "")
        user = request.form.get("user", "")
        password = request.form.get("pass", "")
        svlan = request.form.get("svlan", "")

        # OUTPUT 2 - CONFIG SCRIPT (with colored input values)
        config_script = f"""interface gpon_olt-<span class="input-value">{port}</span>
 onu <span class="input-value">{onu_id}</span> type ZXHN-<span class="input-value">{onu_type}</span> sn <span class="input-value">{sn}</span>
 bind-onu <span class="input-value">{onu_id}</span> profile line HSI-Nolimit
 bind-onu <span class="input-value">{onu_id}</span> profile service HSI-Nolimit
$
interface gpon_onu-{port}:<span class="input-value">{onu_id}</span>
 name <span class="input-value">{user}</span>
$
interface vport-{port}.<span class="input-value">{onu_id}</span>:1
 service-port 1 user-vlan 1000 vlan 11 svlan <span class="input-value">{svlan}</span>
$
pon-onu-mng gpon_onu-{port}:{onu_id}
 security-mgmt 1 state enable mode forward protocol https
 security-mgmt 2 state enable mode forward protocol telnet
 security-mgmt 3 state enable mode forward protocol web
 wan-ip ipv4 mode pppoe auth pap username <span class="input-value">{user}</span> password <span class="input-value">{password}</span> vlan-profile HSI-VLAN host 1
 wan 1 ethuni 1,2,3,4 ssid 1,5 service internet host 1
$"""

        # OUTPUT 1 - ONU TYPE ADD (with colored input values)
        onu_type_script = f"""onu-type ZXHN-<span class="input-value">{onu_type}</span> gpon description 4ETH,2POTS,8WIFI max-tcont 8 max-gemport 32 max-iphost 6 max-ipv6-host 6
onu-type-if ZXHN-{onu_type} eth_0/1
onu-type-if ZXHN-{onu_type} eth_0/2
onu-type-if ZXHN-{onu_type} eth_0/3
onu-type-if ZXHN-{onu_type} eth_0/4
onu-type-if ZXHN-{onu_type} pots_0/1
onu-type-if ZXHN-{onu_type} wifi_0/1
onu-type-if ZXHN-{onu_type} wifi_0/2
onu-type-if ZXHN-{onu_type} wifi_0/3
onu-type-if ZXHN-{onu_type} wifi_0/4
onu-type-if ZXHN-{onu_type} wifi_0/5
onu-type-if ZXHN-{onu_type} wifi_0/6
onu-type-if ZXHN-{onu_type} wifi_0/7
onu-type-if ZXHN-{onu_type} wifi_0/8"""

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ZTE ONU Generator</title>

<style>
:root {{
    --bg: #0f172a;
    --card: rgba(255,255,255,0.06);
    --border: rgba(255,255,255,0.12);
    --text: #f8fafc;
    --muted: #94a3b8;
    --primary: #38bdf8;
    --primary-dark: #0ea5e9;
    --green: #22c55e;
    --input-color: #f472b6;
}}

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: Inter, monospace;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: var(--text);
    min-height: 100vh;
}}

.wrapper {{
    max-width: 1200px;
    margin: auto;
    padding: 30px 20px;
}}

.title {{
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 30px;
    color: var(--primary);
}}

.grid {{
    display: grid;
    grid-template-columns: 1fr 1.3fr;
    gap: 24px;
}}

.card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px;
    backdrop-filter: blur(12px);
}}

.card h2 {{
    margin-top: 0;
    font-size: 20px;
    color: var(--primary);
}}

label {{
    display: block;
    margin: 12px 0 6px;
    font-size: 13px;
    color: var(--muted);
    font-weight: 600;
}}

input {{
    width: 100%;
    padding: 12px 14px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.04);
    color: var(--text);
    outline: none;
    transition: 0.2s;
}}

input:focus {{
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(56,189,248,0.25);
}}

.actions {{
    display: flex;
    gap: 12px;
    margin-top: 20px;
}}

button {{
    flex: 1;
    padding: 12px;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
}}

.generate {{
    background: var(--primary);
    color: #0f172a;
}}

.generate:hover {{
    background: var(--primary-dark);
}}

.copy-btn {{
    background: #1e293b;
    color: var(--text);
    border: 1px solid var(--border);
}}

.copy-btn:hover {{
    background: #334155;
}}

.output-card {{
    margin-bottom: 20px;
}}

.output-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}}

.output-head h3 {{
    margin: 0;
    color: var(--green);
}}

pre {{
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 16px;
    color: #86efac;
    overflow: auto;
    white-space: pre-wrap;
    font-size: 14px;
    line-height: 1.55;
    min-height: 140px;
}}

.input-value {{
    color: var(--input-color);
    font-weight: 700;
}}

.toast {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: var(--primary);
    color: #0f172a;
    padding: 12px 18px;
    border-radius: 12px;
    font-weight: 700;
    display: none;
    z-index: 9999;
    animation: none;
}}

.toast.show {{
    animation: toastIn 0.3s ease-out;
}}

.toast.hide {{
    animation: toastOut 0.3s ease-in;
}}

@keyframes toastIn {{
    0% {{
        opacity: 0;
        transform: translateY(20px);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes toastOut {{
    0% {{
        opacity: 1;
        transform: translateY(0);
    }}
    100% {{
        opacity: 0;
        transform: translateY(20px);
    }}
}}

@media (max-width: 900px) {{
    .grid {{
        grid-template-columns: 1fr;
    }}
}}
</style>
</head>

<body>

<div class="wrapper">
    <div class="title">⚡ ZTE ONU Config Generator</div>

    <div class="grid">

        <div class="card">
            <h2>Input Details</h2>

            <form method="POST">

                <label>PPPoE Username</label>
                <input name="user" value="{user}" placeholder="AN1914" required>

                <label>PPPoE Password</label>
                <input name="pass" value="{password}" placeholder="rlVjfB2q0F" required>

                <label>Serial Number (SN)</label>
                <input name="sn" value="{sn}" placeholder="ZTEGCED95CA6" required>

                <label>ONU Type</label>
                <input name="type" value="{onu_type}" placeholder="F672YV9.1" required>

                <label>Frame / Slot / Port</label>
                <input name="port" value="{port}" placeholder="1/3/15" required>

                <label>ONU ID</label>
                <input name="onu" value="{onu_id}" placeholder="8" required>

                <label>SVLAN</label>
                <input name="svlan" value="{svlan}" placeholder="2502" required>

                <div class="actions">
                    <button class="generate" type="submit">GENERATE</button>
                </div>

            </form>
        </div>

        <div class="card">
            <h2>Generated Outputs</h2>

            <!-- CONFIG SCRIPT FIRST -->

            <div class="output-card">
                <div class="output-head">
                    <h3>1️⃣ ONU Config Script</h3>
                    <button class="copy-btn" type="button"
                        onclick="copyText('configOut')">
                        Copy
                    </button>
                </div>

                <pre id="configOut">{config_script}</pre>
            </div>

            <!-- ONU TYPE SECOND -->

            <div class="output-card">
                <div class="output-head">
                    <h3>2️⃣ ONU Type Add Script</h3>
                    <button class="copy-btn" type="button"
                        onclick="copyText('onuTypeOut')">
                        Copy
                    </button>
                </div>

                <pre id="onuTypeOut">{onu_type_script}</pre>
            </div>

        </div>

    </div>
</div>

<div class="toast" id="toast">Copied!</div>

<script>
const fields = ["port", "type", "sn", "onu", "user", "pass", "svlan"];

// Restore saved values
window.onload = () => {{
    fields.forEach(f => {{
        const el = document.querySelector(`[name="${{f}}"]`);
        const val = localStorage.getItem(f);
        if(el && val) el.value = val;
    }});
}};

// Save while typing
fields.forEach(f => {{
    const el = document.querySelector(`[name="${{f}}"]`);
    if(el) {{
        el.addEventListener("input", () => {{
            localStorage.setItem(f, el.value);
        }});
    }}
}});

// Copy function (preserves HTML spans)
function copyText(id) {{
    const elem = document.getElementById(id);
    const text = elem.innerText.trim();

    if(!text) {{
        showToast("Nothing to copy");
        return;
    }}

    navigator.clipboard.writeText(text).then(() => {{
        showToast("Copied successfully");
    }}).catch(err => {{
        showToast("Failed to copy");
    }});
}}

function showToast(msg) {{
    const toast = document.getElementById("toast");
    
    // Hide any existing animation first
    toast.classList.remove("show", "hide");
    toast.style.display = "none";
    
    // Force reflow
    void toast.offsetWidth;
    
    // Set message and show with animation
    toast.innerText = msg;
    toast.style.display = "block";
    toast.classList.add("show");
    
    // Hide after 2 seconds with animation
    clearTimeout(window.toastTimer);
    window.toastTimer = setTimeout(() => {{
        toast.classList.remove("show");
        toast.classList.add("hide");
        
        setTimeout(() => {{
            toast.style.display = "none";
            toast.classList.remove("hide");
        }}, 300);
    }}, 2000);
}}
</script>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
