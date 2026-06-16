import os
import re
import json
import argparse
from datetime import datetime

def compile_dashboard(company, role, data_path):
    current_date = datetime.now().strftime("%Y-%m")
    folder_safe_name = f"{current_date}-{company.lower().replace(' ', '-')}"
    folder_safe_name = re.sub(r'[^a-z0-9-_]', '', folder_safe_name)
    target_folder = os.path.join("documents", "targets", folder_safe_name)
    os.makedirs(target_folder, exist_ok=True)

    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON data file: {e}")
        return

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prep Terminal: {company}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code:wght@400;600&display=swap');
        
        :root {{
            --bg-color: #050505;
            --surface: rgba(20, 20, 20, 0.6);
            --surface-hover: rgba(40, 40, 40, 0.8);
            --border: rgba(255, 255, 255, 0.1);
            --text-main: #f3f4f6;
            --text-dim: #9ca3af;
            --accent-1: #8b5cf6;
            --accent-2: #ec4899;
            --accent-3: #06b6d4;
            --success: #10b981;
            --font-main: 'Outfit', sans-serif;
            --font-mono: 'Fira Code', monospace;
        }}
        
        * {{ box-sizing: border-box; }}
        body {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(6, 182, 212, 0.15), transparent 25%);
            background-attachment: fixed;
            color: var(--text-main);
            font-family: var(--font-main);
            margin: 0; display: flex; height: 100vh; overflow: hidden;
        }}

        nav {{
            width: 340px; display: flex; flex-direction: column;
            padding: 2rem 1.5rem; border-right: 1px solid var(--border);
            background: rgba(10, 10, 10, 0.5); z-index: 10;
        }}
        .brand {{
            font-size: 1.2rem; font-weight: 800;
            background: linear-gradient(to right, var(--accent-3), var(--accent-1));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 2rem; display: flex; align-items: center; gap: 0.5rem;
        }}
        
        .progress-widget {{ display: flex; align-items: center; gap: 1rem; padding: 1rem; border-radius: 12px; margin-bottom: 2rem; }}
        .circular-chart {{ position: relative; width: 50px; height: 50px; }}
        .circular-chart svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
        .circular-bg {{ fill: none; stroke: var(--border); stroke-width: 3; }}
        .circular-fill {{ fill: none; stroke: url(#gradient); stroke-width: 3; stroke-dasharray: 0 100; stroke-linecap: round; transition: stroke-dasharray 0.8s ease-out; }}
        .percentage {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 0.85rem; font-weight: 800; font-family: var(--font-mono); }}
        .progress-info h4 {{ margin: 0; font-size: 0.9rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; }}
        .progress-info p {{ margin: 0; font-size: 0.8rem; color: var(--success); font-weight: 600; }}

        .nav-section-title {{ font-size: 0.7rem; font-weight: 800; color: var(--text-dim); letter-spacing: 0.15em; text-transform: uppercase; margin: 1.5rem 0 0.5rem 0; padding-left: 0.5rem; }}
        .nav-item {{ padding: 0.8rem 1rem; border-radius: 10px; cursor: pointer; margin-bottom: 0.4rem; transition: all 0.2s ease; color: var(--text-dim); border: 1px solid transparent; }}
        .nav-item:hover {{ background: var(--surface-hover); color: var(--text-main); }}
        .nav-item.active {{ background: rgba(139, 92, 246, 0.1); border: 1px solid var(--border); border-left: 3px solid var(--accent-1); color: var(--text-main); font-weight: 600; }}
        .nav-title {{ font-size: 0.85rem; margin-bottom: 0.15rem; }}
        .nav-meta {{ font-size: 0.7rem; font-family: var(--font-mono); color: var(--accent-3); }}
        
        main {{ flex: 1; padding: 2rem 4rem; overflow-y: auto; position: relative; }}
        .content-container {{ max-width: 950px; margin: 0 auto; padding-bottom: 4rem; }}
        header {{ margin-bottom: 2rem; }}
        h1 {{ font-size: 2.8rem; margin: 0 0 0.5rem 0; font-weight: 800; line-height: 1.1; }}
        .role-badge {{ display: inline-block; padding: 0.4rem 1rem; border-radius: 20px; font-family: var(--font-mono); font-size: 0.85rem; background: rgba(6, 182, 212, 0.1); color: var(--accent-3); border: 1px solid rgba(6, 182, 212, 0.2); }}

        .viewport-card {{ border-radius: 24px; padding: 3rem; position: relative; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); min-height: 550px; display: flex; flex-direction: column; }}
        .controls {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 3rem; }}
        .btn {{ background: var(--surface); border: 1px solid var(--border); color: var(--text-main); padding: 0.7rem 1.5rem; border-radius: 12px; cursor: pointer; transition: all 0.2s; font-family: var(--font-mono); font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem; }}
        .btn:hover:not(:disabled) {{ background: var(--surface-hover); border-color: var(--text-dim); }}
        .btn:disabled {{ opacity: 0.2; cursor: not-allowed; }}
        .btn-primary {{ background: linear-gradient(135deg, var(--accent-1), var(--accent-3)); border: none; color: white; font-weight: 600; }}
        .btn-primary:hover {{ filter: brightness(1.2); box-shadow: 0 0 15px rgba(6, 182, 212, 0.4); }}
        .btn-success {{ background: rgba(16, 185, 129, 0.1); border: 1px solid var(--success); color: var(--success); }}
        .counter {{ font-family: var(--font-mono); font-size: 1rem; font-weight: 600; color: var(--text-dim); }}

        .content-area {{ flex: 1; display: flex; flex-direction: column; gap: 1.5rem; }}
        .question-text {{ font-size: 1.8rem; font-weight: 600; line-height: 1.4; margin-bottom: 1rem; color: white; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
        .info-box {{ background: rgba(0,0,0,0.3); border-radius: 12px; padding: 1.5rem; border: 1px solid var(--border); }}
        .info-label {{ font-size: 0.75rem; font-weight: 800; color: var(--accent-3); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem; }}
        .info-box p {{ margin: 0; font-size: 0.95rem; line-height: 1.6; color: var(--text-dim); }}
        .response-box {{ background: #020617; border-radius: 12px; padding: 2rem; border: 1px solid var(--border); border-left: 4px solid var(--accent-1); margin-top: 1rem; }}
        .response-box p {{ margin: 0; font-family: var(--font-mono); font-size: 0.95rem; line-height: 1.7; color: #e2e8f0; white-space: pre-wrap; }}

        .card-footer {{ margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
        .status-badge {{ display: flex; align-items: center; gap: 0.5rem; font-family: var(--font-mono); font-size: 0.85rem; color: var(--text-dim); padding: 0.5rem 1rem; border-radius: 20px; background: rgba(0,0,0,0.3); }}
        .status-badge.mastered {{ color: var(--success); background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); }}
        
        .glass {{ background: var(--surface); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid var(--border); }}
        .animate-in {{ animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; }}
        @keyframes slideUp {{ 0% {{ opacity: 0; transform: translateY(20px); }} 100% {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body>
    <svg width="0" height="0"><defs><linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#8b5cf6" /><stop offset="100%" stop-color="#06b6d4" /></linearGradient></defs></svg>

    <nav>
        <div class="brand"><i class="fa-solid fa-code"></i> INTERVIEW.OS</div>
        <div class="progress-widget glass">
            <div class="circular-chart">
                <svg viewBox="0 0 36 36">
                    <path class="circular-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    <path class="circular-fill" id="progress-ring" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                </svg>
                <div class="percentage" id="progress-text">0%</div>
            </div>
            <div class="progress-info"><h4>Readiness Score</h4><p id="progress-status">Processing Matrix</p></div>
        </div>
        
        <div class="nav-section-title">Interview Phases</div>
        <div id="sidebar-questions"></div>
        <div class="nav-section-title">Terminology Vault</div>
        <div id="sidebar-glossary"></div>
    </nav>

    <main>
        <div class="content-container">
            <header>
                <h1 id="main-company-title">{company}</h1>
                <div class="role-badge" id="main-role-badge"><i class="fa-solid fa-briefcase"></i> {role}</div>
            </header>

            <div class="viewport-card glass">
                <div class="controls" id="navigation-controls-panel">
                    <button class="btn" onclick="prevItem()" id="prevBtn"><i class="fa-solid fa-arrow-left"></i> Prev</button>
                    <div class="counter" id="counter">01 / 05</div>
                    <button class="btn" onclick="nextItem()" id="nextBtn">Next <i class="fa-solid fa-arrow-right"></i></button>
                </div>

                <div class="content-area animate-in" id="animation-wrapper">
                    <div class="question-text" id="item-title">Loading Dynamic Core Vectors...</div>
                    
                    <div class="info-grid">
                        <div class="info-box">
                            <div class="info-label" id="box-left-label"><i class="fa-solid fa-brain"></i> Interviewer Intent</div>
                            <p id="box-left-text"></p>
                        </div>
                        <div class="info-box">
                            <div class="info-label" id="box-right-label"><i class="fa-solid fa-link"></i> CV Alignment</div>
                            <p id="box-right-text"></p>
                        </div>
                    </div>

                    <div class="response-box">
                        <div class="info-label" id="box-bottom-label" style="color: var(--accent-1);"><i class="fa-solid fa-terminal"></i> Technical Script (Read Aloud)</div>
                        <p id="box-bottom-text"></p>
                    </div>
                </div>

                <div class="card-footer">
                    <div class="status-badge" id="status-badge">
                        <i class="fa-solid fa-circle-notch" id="status-icon"></i> <span id="status-text">Pending Review</span>
                    </div>
                    <button class="btn btn-primary" id="mastery-btn" onclick="toggleMastery()">
                        <i class="fa-solid fa-check"></i> Mark Mastered
                    </button>
                </div>
            </div>
        </div>
    </main>

    <script>
        const dataset = {json.dumps(payload)};
        let currentMode = 'question'; 
        let activeGroupIndex = 0;
        let activeItemIndex = 0;

        // Instantiating memory matrices
        dataset.questions.forEach(q => q.mastered = false);
        if(!dataset.glossary) {{ dataset.glossary = []; }}
        dataset.glossary.forEach(g => g.mastered = false);

        const qCategories = Array.from(new Set(dataset.questions.map(q => q.category)));
        const qGrouped = qCategories.map(cat => ({{ name: cat, items: dataset.questions.filter(q => q.category === cat) }}));

        function calculateOverallMastery() {{
            const total = dataset.questions.length + dataset.glossary.length;
            const mastered = dataset.questions.filter(q => q.mastered).length + dataset.glossary.filter(g => g.mastered).length;
            const percent = total > 0 ? Math.round((mastered / total) * 100) : 0;
            
            document.getElementById('progress-text').innerText = `${{percent}}%`;
            document.getElementById('progress-ring').style.strokeDasharray = `${{percent}}, 100`;
            document.getElementById('progress-status').innerText = percent === 100 ? "Ready to Crush It 🚀" : "Optimization Sandbox";
        }}

        function renderSidebarLists() {{
            const qContainer = document.getElementById('sidebar-questions');
            qContainer.innerHTML = qGrouped.map((cat, i) => `
                <div class="nav-item ${{currentMode === 'question' && i === activeGroupIndex ? 'active' : ''}}" onclick="switchCategory('question', ${{i}})">
                    <div class="nav-title">${{cat.name}}</div>
                    <div class="nav-meta">${{cat.items.filter(item => item.mastered).length}} / ${{cat.items.length}} Mastered</div>
                </div>
            `).join('');

            const gContainer = document.getElementById('sidebar-glossary');
            if(dataset.glossary.length > 0) {{
                gContainer.innerHTML = `
                    <div class="nav-item ${{currentMode === 'glossary' ? 'active' : ''}}" onclick="switchCategory('glossary', 0)">
                        <div class="nav-title">Terms & Core Layouts</div>
                        <div class="nav-meta">${{dataset.glossary.filter(g => g.mastered).length}} / ${{dataset.glossary.length}} Mastered</div>
                    </div>
                `;
            }}
        }}

        function triggerUIReflow() {{
            const wrapper = document.getElementById('animation-wrapper');
            wrapper.classList.remove('animate-in');
            void wrapper.offsetWidth;
            wrapper.classList.add('animate-in');
        }}

        function hydrateViewport() {{
            triggerUIReflow();
            let currentItem;

            if (currentMode === 'question') {{
                const group = qGrouped[activeGroupIndex];
                currentItem = group.items[activeItemIndex];

                document.getElementById('box-left-label').innerHTML = '<i class="fa-solid fa-brain"></i> Interviewer Intent';
                document.getElementById('box-right-label').innerHTML = '<i class="fa-solid fa-link"></i> CV Alignment';
                document.getElementById('box-bottom-label').innerHTML = '<i class="fa-solid fa-terminal"></i> Technical Script (Read Aloud)';

                document.getElementById('item-title').innerText = currentItem.question;
                document.getElementById('box-left-text').innerText = currentItem.intent;
                document.getElementById('box-right-text').innerText = currentItem.alignment;
                document.getElementById('box-bottom-text').innerText = currentItem.response;
                document.getElementById('counter').innerText = `${{String(activeItemIndex + 1).padStart(2, '0')}} / ${{String(group.items.length).padStart(2, '0')}}`;

                document.getElementById('prevBtn').disabled = activeItemIndex === 0;
                document.getElementById('nextBtn').disabled = activeItemIndex === group.items.length - 1;
            }} else {{
                currentItem = dataset.glossary[activeItemIndex];

                document.getElementById('box-left-label').innerHTML = '<i class="fa-solid fa-book"></i> Clean English Definition';
                document.getElementById('box-right-label').innerHTML = '<i class="fa-solid fa-crosshairs"></i> Why They Ask';
                document.getElementById('box-bottom-label').innerHTML = '<i class="fa-solid fa-comments"></i> Conversational Application';

                document.getElementById('item-title').innerText = currentItem.term;
                document.getElementById('box-left-text').innerText = currentItem.definition;
                document.getElementById('box-right-text').innerText = currentItem.why_they_ask;
                document.getElementById('box-bottom-text').innerText = currentItem.conversational_script;
                document.getElementById('counter').innerText = `${{String(activeItemIndex + 1).padStart(2, '0')}} / ${{String(dataset.glossary.length).padStart(2, '0')}}`;

                document.getElementById('prevBtn').disabled = activeItemIndex === 0;
                document.getElementById('nextBtn').disabled = activeItemIndex === dataset.glossary.length - 1;
            }}

            const btn = document.getElementById('mastery-btn');
            const badge = document.getElementById('status-badge');
            const statusIcon = document.getElementById('status-icon');
            const statusText = document.getElementById('status-text');

            if (currentItem.mastered) {{
                btn.className = "btn btn-success";
                btn.innerHTML = '<i class="fa-solid fa-rotate-left"></i> Needs Review';
                badge.className = "status-badge mastered";
                statusIcon.className = "fa-solid fa-circle-check";
                statusText.innerText = "Locked in Memory";
            }} else {{
                btn.className = "btn btn-primary";
                btn.innerHTML = '<i class="fa-solid fa-check"></i> Mark Mastered';
                badge.className = "status-badge";
                statusIcon.className = "fa-solid fa-circle-notch fa-spin";
                statusText.innerText = "Pending Review";
            }}

            calculateOverallMastery();
            renderSidebarLists();
        }}

        function switchCategory(mode, index) {{
            currentMode = mode;
            activeGroupIndex = index;
            activeItemIndex = 0;
            hydrateViewport();
        }}

        function nextItem() {{
            const limit = currentMode === 'question' ? qGrouped[activeGroupIndex].items.length : dataset.glossary.length;
            if (activeItemIndex < limit - 1) {{ activeItemIndex++; hydrateViewport(); }}
        }}

        function prevItem() {{
            if (activeItemIndex > 0) {{ activeItemIndex--; hydrateViewport(); }}
        }}

        function toggleMastery() {{
            let currentItem = currentMode === 'question' ? qGrouped[activeGroupIndex].items[activeItemIndex] : dataset.glossary[activeItemIndex];
            currentItem.mastered = !currentItem.mastered;
            hydrateViewport();
        }}

        document.addEventListener('DOMContentLoaded', hydrateViewport);
    </script>
</body>
</html>
"""
    
    output_filename = os.path.join(target_folder, "prep_dashboard.html")
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"📊 Success: Elite Pro Terminal generated at: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--data", required=True)
    args = parser.parse_args()
    compile_dashboard(args.company, args.role, args.data)