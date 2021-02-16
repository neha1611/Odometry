from app import app

from layout.layout import layout

from routes import render_page_content

from layout.sidebar_callbacks import toggle_collapse, toggle_classname

from settings.config import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK

app.layout = layout

if __name__ == "__main__":
    app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK
    )
