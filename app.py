import streamlit as st


def run():
    st.title("Datatables.net Ajax Test App")
    st.markdown("""
    - Simple app showing the use of st_datatable_net with an Ajax data source.
    - This component is based on the Datatable.net library.
    - In this example, the data is loaded from the dummyjson.com API with a delay of 2 seconds.
    - By using Ajax, Streamlit content, including the data table, is rendered immediately but the data is loaded aynchronously.
    - Clicking the Refresh Button illustrates the delay in the data loading while not impacting the display of other Streamlit content.
    """)
    main_container = st.container()
    st.header("Code")
    with st.expander("Code", expanded=True):
        with st.echo():
            # import streamlit as st
            from streamlit_datatables_net import st_datatable

            @st.dialog("Product Data", width="large")
            def show_data():
                if "data" in st.session_state["datatable"]:
                    st.json(st.session_state["datatable"]["data"], expanded=1)

            def click_handler():
                if "data" in st.session_state["datatable"]:
                    show_data()

            def get_datatable_options():
                options = {}
                options["columns"] = [
                    {"data": "id", "title": "ID"},
                    {"data": "thumbnail",
                        "render": """function showThumbnail(data, type, row, meta) {return '<img src="' + data + '" height="60"/>'}"""},
                    {"data": "title", "title": "Title"},
                    {"data": "description", "title": "Description",
                        "render": "function truncateText(data, type, row, meta) {return '<span title="' + data + '">' + data.substr(0, 20) + '...</span>';}"},
                    {"data": "price", "title": "Price",
                        "render": "function showCurrencySign( data, type, row ) {return '$'+ data;}"},
                    {"data": "rating", "title": "Rating"},
                    {"data": "stock", "title": "Stock"},
                    {"data": "category", "title": "Category"},
                ]
                url = "https://dummyjson.com/products?delay=2000"
                options["ajax"] = {
                    "url": url,
                    "dataSrc": "products",
                    "type": "GET"
                }
                refresh_button = {"text": "Refresh Table",
                                  "action": "function reloadTableFromAjax(e, dt, node, config, cb){dt.ajax.reload()}"}
                options["buttons"] = [refresh_button]

                options["layout"] = {
                    "topStart": ["pageLength", "buttons"],
                    'topEnd': "search",
                    'bottomStart': 'info',
                    'bottomEnd': 'paging'
                }
                options["processing"] = True
                return options

            with main_container:
                st.header("Click on a row to view product details")
                options = get_datatable_options()
                st_datatable(None, options=options, key="datatable",
                             enable_diagnostics=True, on_select=click_handler)


if __name__ == "__main__":
    st.set_page_config(initial_sidebar_state="expanded", layout="wide")
    run()