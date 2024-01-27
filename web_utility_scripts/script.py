from pathlib import Path
import json
import time
from st_aggrid import AgGrid
import pandas as pd
import streamlit as st


MAIN_DIR = Path(__file__).parent.parent
RESOURCES_DIR = MAIN_DIR / "resources"
DATA_DIR = RESOURCES_DIR / "data"
JSON_DIR = DATA_DIR / "jsons"

full_table_width = True

# df = pd.DataFrame(
#     [
#         {"command": "st.selectbox", "rating": 4, "some_bool": True},
#         {"command": "st.balloons", "rating": 5, "some_bool": False},
#         {"command": "st.time_input", "rating": 3, "some_bool": True},
#     ]
# )

# records_list = json.loads(df.to_json(orient="records"))
# for i, record in enumerate(records_list):
#     (JSON_DIR / f"{i}.json").write_text(json.dumps(record))

select_column = "select"
id_column = "id"
records_list = [
    {select_column: False, id_column: i.stem} | json.loads(i.read_text())
    for i in JSON_DIR.glob("*.json")
]
df = pd.DataFrame(records_list)

if df.empty:
    st.stop()

# id_hidden_df = df[[col for col in df.columns if col != "id"]]

edited_df = st.data_editor(
    df,
    hide_index=True,
    use_container_width=full_table_width,
    column_order=[c for c in df.columns if c != id_column],
)
if edited_df.empty:
    st.stop()


# st.dataframe(edited_df)


_, del_btn_col, _, add_btn_col, _ = st.columns(5, gap="large")
select_filter = edited_df[select_column] == True
selected_records = df[select_filter]
with del_btn_col:
    if st.button(
        "Delete",
        key="delete_item_btn",
        disabled=selected_records.empty,
        use_container_width=True,
    ):
        edited_df[select_filter][id_column].apply(
            lambda x: (JSON_DIR / f"{str(x)}.json").unlink(missing_ok=True)
        )
        st.rerun()

added_items = pd.DataFrame()
with add_btn_col:
    if st.button(
        "Add",
        key="add_item_btn",
        disabled=selected_records.empty,
        use_container_width=True,
    ):
        added_items = edited_df[select_filter]

try:
    if not added_items.empty:
        st.caption("ADDED DATA")
        st.dataframe(
            added_items.drop(columns=[select_column]),
            use_container_width=full_table_width,
            hide_index=True,
            column_order=[c for c in df.columns if c not in [id_column, select_column]],
        )

except NameError:
    pass


if st.button(
    label="submit records",
    type="primary",
    disabled=added_items.empty,
    use_container_width=True,
):
    st.success("records are successfully submitted!")
