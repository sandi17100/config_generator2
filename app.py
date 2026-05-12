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
    config = ""

    if request.method == "POST":
        port = request.form.get("port", "")
        onu_type = request.form.get("type", "")
        sn = request.form.get("sn", "")
        onu_id = request.form.get("onu", "")
        user = request.form.get("user", "")
        password = request.form.get("pass", "")
        svlan = request.form.get("svlan", "")

        config = f"""interface gpon_olt-{port}
  onu {onu_id} type ZXHN-{onu_type} sn {sn}
  bind-onu {onu_id} profile line HSI-Nolimit
  bind-onu {onu_id} profile service HSI-Nolimit
$
  interface gpon_onu-{port}:{onu_id}
  name {user}
$
  interface vport-{port}.{onu_id}:1
  service-port 1 user-vlan 1000 vlan 11 svlan {svlan}
$
pon-onu-mng gpon_onu-{port}:{onu_id}
  security-mgmt 1 state enable mode forward protocol https
  security-mgmt 2 state enable mode forward protocol telnet
  security-mgmt 3 state enable mode forward protocol web
  wan-ip ipv4 mode pppoe auth pap username {user} password {password} vlan-profile HSI-VLAN host 1
  wan 1 ethuni 1,2,3,4 ssid 1,5 service internet host 1
$
"""

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>ZTE ONU CONFIG GENERATOR</title>

<style>
:root {{
    --bg: #FFFFFF;
    --panel: #F8FAFC;
    --panel-2: #F1F5F9;
    --border: #E2E8F0;
    --text: #1E293B;
    --muted: #64748B;
    --sky-blue: #87CEEB;
    --dark-blue: #1E3A8A;
}}

body {{
    margin: 0;
    font-family: monospace;
    background: var(--bg);
    font-size: 20px;
    color: var(--text);
}}

.top {{
    padding: 20px;
    border-bottom: 2px solid var(--border);
    text-align: center;
    background: var(--panel);
    font-weight: bold;
}}

.container {{
    display: flex;
    min-height: 100vh;
}}

.left {{
    width: 35%;
    padding: 15px;
    border-right: 1px solid var(--border);
    background: var(--panel);
}}

.right {{
    width: 65%;
    padding: 15px;
}}

input {{
    width: 100%;
    padding: 10px;
    margin: 5px 0;
    background: var(--panel-2);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 6px;
    box-sizing: border-box;
}}

input::placeholder {{
    color: var(--muted);
}}

button {{
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border: none;
    cursor: pointer;
    font-weight: bold;
    border-radius: 6px;
    transition: 0.2s;
}}

.gen {{
    background: var(--sky-blue);
    color: var(--dark-blue);
}}

.gen:hover {{
    background: #6BB9D8;
}}

.copy {{
    background: var(--dark-blue);
    color: white;
}}

.copy:hover {{
    background: #1E40AF;
}}

pre {{
    background: black;
    color: #00FF00;
    border: 1px solid #00AA00;
    padding: 15px;
    height: 90%;
    overflow: auto;
    white-space: pre-wrap;
    border-radius: 6px;
    font-size: 15px;
    line-height: 1.5;
}}

.btn-group {{
    display: flex;
    gap: 10px;
    margin-top: 10px;
}}

.btn-group button {{
    flex: 1;
}}

label {{
    display: block;
    margin-top: 12px;
    margin-bottom: 5px;
    font-size: 13px;
    font-weight: bold;
}}

#toast {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #1E3A8A;
    color: white;
    padding: 12px 18px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    display: none;
    z-index: 9999;
}}
</style>
</head>

<body>

<div class="top">ZTE ONU CONFIG GENERATOR</div>

<div class="container">

    <div class="left">
        <form method="POST" onsubmit="saveInputs()">

            <label>frame/slot/port</label>
            <input name="port" value="{port}" placeholder="1/3/15" required>

            <label>ONU Type (F671Y)</label>
            <input name="type" value="{onu_type}" placeholder="F671Y" required>

            <label>SN</label>
            <input name="sn" value="{sn}" placeholder="ZTEGCED95CA6" required>

            <label>ONU ID</label>
            <input name="onu" value="{onu_id}" placeholder="8" required>

            <label>Username</label>
            <input name="user" value="{user}" placeholder="AN1914" required>

            <label>Password</label>
            <input name="pass" value="{password}" placeholder="rlVjfB2q0F" required>

            <label>SVLAN</label>
            <input name="svlan" value="{svlan}" placeholder="2502" required>

            <div class="btn-group">
                <button class="gen" type="submit">GENERATE</button>
                <button class="copy" type="button" onclick="copyAll()">COPY ALL</button>
            </div>

        </form>
    </div>

    <div class="right">
        <pre id="out">{config}</pre>
    </div>

</div>

<div id="toast"></div>

<script>
const fields = ["port", "type", "sn", "onu", "user", "pass", "svlan"];

// Restore saved inputs
window.onload = function() {{
    fields.forEach(field => {{
        let input = document.querySelector(`[name="${{field}}"]`);
        let savedValue = localStorage.getItem(field);

        if (input && savedValue) {{
            input.value = savedValue;
        }}
    }});
}};

// Save while typing
fields.forEach(field => {{
    let input = document.querySelector(`[name="${{field}}"]`);
    if (input) {{
        input.addEventListener("input", function() {{
            localStorage.setItem(field, this.value);
        }});
    }}
}});

// Save again before submit
function saveInputs() {{
    fields.forEach(field => {{
        let input = document.querySelector(`[name="${{field}}"]`);
        if (input) {{
            localStorage.setItem(field, input.value);
        }}
    }});
}}

// Copy config
function copyAll() {{
    let text = document.getElementById("out").innerText;

    if (!text || text.trim() === "") {{
        showToast("Nothing to copy");
        return;
    }}

    navigator.clipboard.writeText(text)
        .then(() => {{
            showToast("COPIED SUCCESSFULLY");
        }})
        .catch(() => {{
            showToast("Copy failed");
        }});
}}

// Toast popup
function showToast(message) {{
    let toast = document.getElementById("toast");
    toast.innerText = message;
    toast.style.display = "block";

    clearTimeout(window.toastTimer);
    window.toastTimer = setTimeout(() => {{
        toast.style.display = "none";
    }}, 2000);
}}
</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
