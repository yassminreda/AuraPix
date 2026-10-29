"""Edit LIGHT/DARK for colors; edit CSS below for layout."""
LIGHT = dict(bg='#F8F7F4', card='#FFFFFF', text='#292632', muted='#86808F', primary='#7961AA', soft='#F0EAF7', border='#E7E0EF', field='#F8F6FA')
DARK = dict(bg='#18161E', card='#24212B', text='#F3EEF9', muted='#B8AFC5', primary='#B39BDC', soft='#332B43', border='#433A50', field='#2C2735')

def css(dark=False, rtl=False):
    c = DARK if dark else LIGHT
    values = ';'.join(f'--ap-{k}:{v}' for k,v in c.items())
    direction = 'rtl' if rtl else 'ltr'
    return '<style>:root{' + values + '}\n' + BASE.replace('DIRECTION', direction) + '</style>'

BASE = '''
html,body,.stApp {background:var(--ap-bg);color:var(--ap-text);font-family:"Segoe UI",sans-serif;}
h1,h2,h3,p,label,span {letter-spacing:0;}
.stApp p,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp [data-testid="stWidgetLabel"] {color:var(--ap-text);}
[data-testid="stHeader"] {background:var(--ap-bg)!important;color:var(--ap-text)!important;}
[data-testid="stToolbar"] button,[data-testid="stMainMenu"] button,[data-testid="stSidebarCollapseButton"] button,[data-testid="stExpandSidebarButton"] button {color:var(--ap-text)!important;}
[data-testid="stToolbar"] svg,[data-testid="stMainMenu"] svg {color:var(--ap-text)!important;fill:currentColor!important;}
[data-testid="stPopoverBody"],[data-baseweb="popover"]>div,[data-baseweb="menu"] {background:var(--ap-card)!important;color:var(--ap-text)!important;}
[data-testid="stSidebar"] {background:var(--ap-card);border-right:1px solid var(--ap-border);min-width:240px;max-width:260px;}
[data-testid="stSidebar"]>div {padding-top:2rem;}
[data-testid="stMainBlockContainer"] {max-width:1120px;padding:2rem 3rem 4rem;direction:DIRECTION;}
.ap-logo {display:flex;align-items:center;gap:10px;margin:0 0 2rem;}
.ap-logo-icon {width:38px;height:38px;background:var(--ap-primary);color:var(--ap-card);display:grid;place-items:center;border-radius:10px;font-size:24px;}
.ap-logo strong {font-size:19px;color:var(--ap-text);}.ap-logo small {display:block;font-size:11px;color:var(--ap-muted);}
[data-testid="stSidebar"] [role="radiogroup"] {gap:5px;}
[data-testid="stSidebar"] [role="radiogroup"] label {padding:8px 10px;border-radius:9px;width:100%;}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:var(--ap-soft);border-inline-start:3px solid var(--ap-primary);}
.ap-side-settings {margin-top:clamp(70px,25vh,280px);}
.ap-status {border:1px solid var(--ap-border);border-radius:20px;padding:8px 12px;color:var(--ap-muted);font-size:11px;margin-bottom:15px;}
.ap-status b {color:var(--ap-primary);}
.ap-hero {border:1px solid var(--ap-border);background:var(--ap-card);border-radius:22px;padding:32px;display:grid;grid-template-columns:1.15fr 1fr;gap:24px;align-items:center;margin-bottom:20px;}
.ap-eyebrow {display:inline-block;font-size:10px;font-weight:700;color:var(--ap-primary);background:var(--ap-soft);border-radius:20px;padding:5px 10px;}
.ap-hero h1 {font-size:36px;line-height:1.2;margin:16px 0;color:var(--ap-text);font-weight:700;}
.ap-hero p {font-size:14px;line-height:1.65;color:var(--ap-muted);margin:0;}
.ap-hero img {width:100%;aspect-ratio:1.6;object-fit:cover;border-radius:18px;}
.ap-notice {border:1px solid var(--ap-border);background:var(--ap-soft);border-radius:16px;padding:12px 16px;margin-bottom:20px;font-size:12px;color:var(--ap-text);}
.ap-notice small {display:block;color:var(--ap-muted);margin-top:4px;}
[data-testid="stVerticalBlockBorderWrapper"]>div {background:var(--ap-card);border-color:var(--ap-border)!important;border-radius:20px!important;}
.ap-heading {display:flex;gap:10px;align-items:start;margin-bottom:10px;}
.ap-icon {background:var(--ap-soft);color:var(--ap-primary);width:32px;height:32px;flex:none;border-radius:10px;display:grid;place-items:center;font-size:19px;}
.ap-heading strong {font-size:15px;color:var(--ap-text);}.ap-heading small {display:block;font-size:12px;color:var(--ap-muted);margin-top:3px;}
button[data-variant="segmented_control"] p,[data-testid="stFileUploaderDropzone"] button p {color:var(--ap-primary)!important;}
textarea::placeholder {color:var(--ap-muted)!important;}
textarea,input,[data-baseweb="select"]>div {background:var(--ap-field)!important;color:var(--ap-text)!important;border-color:var(--ap-border)!important;}
[data-testid="stFileUploaderDropzone"] {background:var(--ap-field);border:2px dashed var(--ap-border);border-radius:16px;min-height:240px;display:flex;flex-direction:column;justify-content:center;text-align:center;gap:12px;}
[data-testid="stFileUploaderDropzone"]>div {display:flex;flex-direction:column;align-items:center;}
[data-testid="stFileUploaderDropzone"] small {color:var(--ap-muted);}
.stButton button,.stDownloadButton button,[data-testid="stFileUploaderDropzone"] button {border-radius:12px;border-color:var(--ap-border);background:var(--ap-card)!important;color:var(--ap-primary)!important;}
.stButton button[kind="primary"] {background:var(--ap-primary);color:var(--ap-card);border:0;min-height:44px;}
.stButton button[kind="primary"] p {color:var(--ap-card)!important;}
button[data-variant="segmented_control"] {background:var(--ap-soft)!important;color:var(--ap-text)!important;border-color:var(--ap-border)!important;}
button[data-variant="segmented_control"][aria-checked="true"] {background:var(--ap-card)!important;}
.ap-empty {background:var(--ap-field);border:1px dashed var(--ap-border);border-radius:18px;min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:26px;margin:4px 0 16px;}
.ap-empty strong {font-size:14px;margin:12px 0 6px;color:var(--ap-text);}.ap-empty p {font-size:12px;color:var(--ap-muted);max-width:280px;}
.ap-about {background:var(--ap-card);border:1px solid var(--ap-border);border-radius:20px;padding:32px;margin-bottom:24px;}
.ap-about h1 {font-size:29px;margin:14px 0;}.ap-about p,.ap-info p {color:var(--ap-muted);font-size:14px;line-height:1.75;}
.ap-info {background:var(--ap-card);border:1px solid var(--ap-border);border-radius:18px;padding:20px;height:100%;}
.ap-info h3 {font-size:16px;color:var(--ap-text);margin:14px 0 10px;}.ap-tags {display:flex;flex-wrap:wrap;gap:5px;}.ap-tags span {background:var(--ap-soft);color:var(--ap-primary);font-size:10px;padding:4px 8px;border-radius:14px;}
.ap-grid {display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:28px;}.ap-flow {display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px;}.ap-flow .ap-info {padding:16px;}.ap-flow h3 {font-size:13px;}.ap-flow p {font-size:12px;}.ap-step-number {float:right;color:var(--ap-muted);font-size:11px;}
[data-testid="stImage"] img {border-radius:12px;}
@media(max-width:800px) {[data-testid="stMainBlockContainer"]{padding:1.5rem 1rem 3rem;}.ap-hero {grid-template-columns:1fr;padding:24px;}.ap-hero h1 {font-size:29px;}.ap-hero img{max-height:180px;}.ap-grid{grid-template-columns:1fr;}.ap-flow{grid-template-columns:1fr 1fr;}.ap-side-settings{margin-top:40px;}}
'''
