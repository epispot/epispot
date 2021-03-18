<%!
    from pdoc.html_helpers import minify_css
%>
<%def name="homelink()" filter="minify_css">
    .homelink {
        display: block;
        font-size: 2em;
        font-weight: bold;
        color: white;
    }
    .homelink:hover {
        color: #e82;
    }
    
</%def>

<style>${homelink()}</style>
<link rel="apple-touch-icon" sizes="180x180" href="https://epispot.github.io/images/epispotfavicon.png">
<link rel="icon" type="image/png" sizes="32x32" href="https://epispot.github.io/images/epispotfavicon.png">
<meta name="theme-color" content="#ffffff">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/docsearch.js@2/dist/cdn/docsearch.min.css" />
