import os
import logging
import datetime
from flask import Flask, jsonify, render_template_string

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)

# Environment Configurations
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
ENV = os.getenv("FLASK_ENV", "production")
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1")

# Single-file Modern Dashboard Template (HTML/CSS/JS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS DevOps Automation Platform</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0d1117;
            --panel: #161b22;
            --border: #30363d;
            --text-main: #f0f6fc;
            --text-sub: #8b949e;
            --primary: #58a6ff;
            --primary-hover: #1f6feb;
            --success: #2ea043;
            --success-bg: rgba(46, 160, 67, 0.15);
            --accent: #ff9900;
        }

        .light-theme {
            --bg: #f6f8fa;
            --panel: #ffffff;
            --border: #d0d7de;
            --text-main: #1f2328;
            --text-sub: #656d76;
            --primary: #0969da;
            --primary-hover: #0349b4;
            --success: #1a7f37;
            --success-bg: rgba(26, 127, 55, 0.15);
            --accent: #ec7211;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        .dashboard {
            width: 100%;
            max-width: 900px;
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 32px;
            border-bottom: 1px solid var(--border);
        }

        .logo-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .aws-badge {
            background: var(--accent);
            color: #000;
            font-weight: 700;
            font-size: 0.75rem;
            padding: 4px 8px;
            border-radius: 4px;
            text-transform: uppercase;
        }

        .title {
            font-size: 1.25rem;
            font-weight: 600;
        }

        .theme-toggle {
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s;
        }

        .theme-toggle:hover {
            border-color: var(--primary);
            color: var(--primary);
        }

        .content {
            padding: 32px;
        }

        .status-banner {
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--success-bg);
            border: 1px solid var(--success);
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 28px;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            background-color: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }

        .card {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            padding: 20px;
            border-radius: 8px;
        }

        .card-label {
            font-size: 0.8rem;
            color: var(--text-sub);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }

        .card-value {
            font-size: 1.1rem;
            font-weight: 600;
        }

        .log-section {
            background: rgba(0,0,0,0.2);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            font-family: monospace;
            font-size: 0.85rem;
            color: var(--text-sub);
        }

        .log-line {
            margin-bottom: 6px;
        }

        .log-line:last-child { margin-bottom: 0; }
        .log-time { color: var(--primary); }

        .footer {
            padding: 16px 32px;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-sub);
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <div class="logo-group">
                <span class="aws-badge">AWS</span>
                <span class="title">DevOps Automation Platform</span>
            </div>
            <button class="theme-toggle" onclick="toggleTheme()">Toggle Theme</button>
        </div>

        <div class="content">
            <div class="status-banner">
                <div class="status-dot"></div>
                <div style="font-weight: 500;">Platform Online & Health Check Passing</div>
            </div>

            <div class="grid">
                <div class="card">
                    <div class="card-label">Environment</div>
                    <div class="card-value">{{ environment }}</div>
                </div>
                <div class="card">
                    <div class="card-label">Health Route</div>
                    <div class="card-value" style="color: var(--success);">/health (200 OK)</div>
                </div>
                <div class="card">
                    <div class="card-label">Server Time</div>
                    <div class="card-value" id="time-display">{{ server_time }}</div>
                </div>
            </div>

            <div class="log-section">
                <div class="log-line"><span class="log-time">[{{ server_time }}]</span> [INFO] Flask application initialized.</div>
                <div class="log-line"><span class="log-time">[{{ server_time }}]</span> [INFO] Route GET / routed successfully.</div>
                <div class="log-line"><span class="log-time">[{{ server_time }}]</span> [INFO] Target group health checks active.</div>
            </div>
        </div>

        <div class="footer">
            <span>Powered by Flask & AWS ECS/App Runner</span>
            <span>Status: Active</span>
        </div>
    </div>

    <script>
        function toggleTheme() {
            document.body.classList.toggle('light-theme');
        }

        // Live clock update
        setInterval(() => {
            const now = new Date();
            const timeString = now.toISOString().split('T')[1].slice(0, 8) + ' UTC';
            document.getElementById('time-display').innerText = timeString;
        }, 1000);
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    """Render the automated modern UI platform dashboard."""
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S UTC")
    return render_template_string(
        HTML_TEMPLATE,
        environment=ENV.upper(),
        server_time=now_utc
    )

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint required for AWS Target Groups / ALB."""
    return jsonify({
        "status": "healthy",
        "service": "aws-devops-automation-platform"
    }), 200

if __name__ == "__main__":
    app.logger.info(f"Starting application UI on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)