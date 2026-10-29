"""AuraPix — run with: streamlit run app.py"""
import base64
import hashlib
from html import escape
from pathlib import Path
from io import BytesIO
import streamlit as st
from PIL import Image, ImageOps
from styles import css
from i18n import translations
from logic import RESULT_COUNTS, SUPPORTED_TYPES, selected_count
import models

st.set_page_config(page_title='AuraPix', page_icon='✨', layout='wide')
ss = st.session_state
ss.setdefault('lang', 'en')
ss.setdefault('dark', False)
t = translations(ss.lang)

with st.sidebar:
    st.markdown('<div class="ap-logo"><div class="ap-logo-icon">◉</div><div><strong>AuraPix</strong><small>' + t['engine'] + '</small></div></div>', unsafe_allow_html=True)
    page = st.radio('Navigation', ['search', 'caption', 'about'], format_func=lambda p: ['⌕  ', '▧  ', 'ⓘ  '][['search','caption','about'].index(p)] + t['nav'][['search','caption','about'].index(p)], label_visibility='collapsed', key='page')
    st.markdown('<div class="ap-side-settings"><div class="ap-status"><b>●</b> '+t['status']+'</div></div>', unsafe_allow_html=True)
    language = st.segmented_control(t['language'], ['en','ar'], format_func=lambda x: 'English' if x=='en' else 'العربية', default=ss.lang, key='language_choice')
    if language and language != ss.lang:
        ss.lang = language
        st.rerun()
    dark = st.toggle(t['dark'], value=ss.dark)
    if dark != ss.dark:
        ss.dark = dark
        st.rerun()

st.markdown(css(ss.dark, ss.lang=='ar'), unsafe_allow_html=True)

def heading(icon, title, subtitle=''):
    st.markdown(f'<div class="ap-heading"><div class="ap-icon">{icon}</div><div><strong>{escape(title)}</strong><small>{escape(subtitle)}</small></div></div>', unsafe_allow_html=True)

def empty(title, body, icon='▧'):
    st.markdown(f'<div class="ap-empty"><div class="ap-icon">{icon}</div><strong>{escape(title)}</strong><p>{escape(body)}</p></div>', unsafe_allow_html=True)

def read_images(files):
    output = []
    for f in files:
        try:
            with Image.open(BytesIO(f.getvalue())) as image:
                image = ImageOps.exif_transpose(image).convert('RGB')
                image.thumbnail((1600,1600))
                output.append((f.name, image.copy()))
        except (OSError, ValueError, Image.DecompressionBombError) as error:
            st.warning(t['bad_image']+' '+f.name)
    return output

def signature(files):
    return hashlib.sha256(b''.join(f.name.encode()+f.getvalue() for f in files)).hexdigest()

def info(icon,title,body,tags=None):
    tag_html = '<div class="ap-tags">'+''.join('<span>'+escape(x)+'</span>' for x in (tags or []))+'</div>'
    return f'<article class="ap-info"><div class="ap-icon">{icon}</div><h3>{escape(title)}</h3><p>{escape(body)}</p>{tag_html}</article>'

if page != 'about':
    image_data = base64.b64encode((Path(__file__).parent/'assets/network.jpg').read_bytes()).decode()
    st.markdown(f'<section class="ap-hero"><div><span class="ap-eyebrow">✧ {t["eyebrow"]}</span><h1>{t["title"]}</h1><p>{t["subtitle"]}</p></div><img src="data:image/jpeg;base64,{image_data}" alt="Connected image collection" /></section>', unsafe_allow_html=True)
    st.markdown(f'<div class="ap-notice">⚗ &nbsp; {t["notice"]}<small>{t["notice_body"]}</small></div>', unsafe_allow_html=True)

if page == 'search':
    left,right = st.columns([1.2,1],gap='medium')
    with left:
        with st.container(border=True):
            heading('▧',t['gallery'],t['gallery_sub'])
            files = st.file_uploader(t['gallery'],type=list(SUPPORTED_TYPES),accept_multiple_files=True,label_visibility='collapsed',key='gallery_files')
            images = read_images(files)
            if images:
                cols = st.columns(3)
                for i,(name,image) in enumerate(images):
                    cols[i%3].image(image,caption=name,use_container_width=True)
    with right:
        with st.container(border=True):
            heading('☷',t['describe'])
            query = st.text_area(t['query'],placeholder=t['placeholder'],height=130,key='query')
            count = st.segmented_control(t['count'],list(RESULT_COUNTS),default=5,key='result_count')
            search = st.button(t['search'],icon=':material/search:',type='primary',use_container_width=True)
    current_sig = signature(files)
    if ss.get('search_sig') != current_sig:
        ss.pop('results',None)
    if search:
        if not images:
            st.error(t['error_images'])
        elif not query.strip():
            st.error(t['error_query'])
        else:
            with st.spinner(t['working']):
                try:
                    ss.results = models.search_images(query.strip(),[im for _,im in images],selected_count(count or 5,len(images)))
                    ss.search_sig = current_sig
                except Exception as error:
                    st.error(t['error_model'])
                    with st.expander('Technical details'):
                        st.code(str(error))
    st.subheader(t['results'])
    if ss.get('results'):
        st.caption(t['score_note'])
        cols = st.columns(3)
        for rank,(index,score) in enumerate(ss.results,1):
            with cols[(rank-1)%3]:
                with st.container(border=True):
                    st.image(images[index][1],use_container_width=True)
                    st.write(f'{t["rank"]} {rank} · {images[index][0]}')
                    st.caption(f'{t["similarity"]}: {score:.3f}')
                    st.progress(max(0.0,min(1.0,score)))
    else:
        empty(t['ready'] if images else t['empty'],t['ready_sub'] if images else t['empty_sub'])
elif page == 'caption':
    left,right = st.columns(2,gap='medium')
    with left:
        with st.container(border=True):
            heading('▧',t['upload'],t['upload_sub'])
            file = st.file_uploader(t['upload'],type=list(SUPPORTED_TYPES),label_visibility='collapsed',key='caption_file')
            images = read_images([file]) if file else []
            sig = signature([file]) if file else ''
            if ss.get('caption_sig') != sig:
                ss.pop('caption',None)
            if images:
                st.image(images[0][1],use_container_width=True)
            go = st.button(t['generate'],icon=':material/auto_awesome:',type='primary',use_container_width=True)
            if go:
                if not images:
                    st.error(t['error_images'])
                else:
                    with st.spinner(t['working']):
                        try:
                            ss.caption = models.caption_image(images[0][1])
                            ss.caption_sig = sig
                        except Exception as error:
                            st.error(t['error_model'])
                            with st.expander('Technical details'):
                                st.code(str(error))
    with right:
        with st.container(border=True):
            heading('▤',t['generated'])
            if ss.get('caption'):
                st.code(ss.caption,language=None,wrap_lines=True)
                st.download_button(t['download'],ss.caption,file_name='AuraPix_caption.txt',mime='text/plain',icon=':material/download:',use_container_width=True)
            else:
                empty(t['no_caption'],t['no_caption_sub'],'▤')
            st.caption(t['caption_note'])
else:
    st.markdown(f'<section class="ap-about"><span class="ap-eyebrow">{t["about_eyebrow"]}</span><h1>{t["about_title"]}</h1><p>{t["about_body"]}</p></section>',unsafe_allow_html=True)
    st.subheader(t['models'])
    st.markdown('<div class="ap-grid">'+info('♧',t['clip_title'],t['clip_body'],t['clip_tags'])+info('▤',t['blip_title'],t['blip_body'],t['blip_tags'])+'</div>',unsafe_allow_html=True)
    st.subheader(t['workflow'])
    steps = ''
    for i,(title,body) in enumerate(zip(t['steps'],t['step_body']),1):
        steps += f'<article class="ap-info"><span class="ap-step-number">{i:02d}</span><div class="ap-icon">{["▧","T","◉","☷"][i-1]}</div><h3>{title}</h3><p>{body}</p></article>'
    st.markdown('<div class="ap-flow">'+steps+'</div>',unsafe_allow_html=True)
    st.markdown('<div class="ap-grid">'+info('▱',t['dataset'],t['dataset_body'])+info('▣',t['architecture'],t['architecture_body'])+'</div>',unsafe_allow_html=True)
