# import libraries
import io
import json
import time
import zipfile
import streamlit as st
from PIL import Image

@st.cache
# defined functions
def adjust_orientation(image):
    orientation = 274 
    exif = image._getexif()
    try:
        if exif:
            exif = dict(exif.items())
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
        return image
    except:
        pass
    return image

def api(image, values):
    result = {
        "ok": True,
        "diag": "Thalassemia"
    }
    return result


# Start an app
st.set_page_config(page_title="Title", page_icon="💡")

st.title("Title of the project")
st.write("Description - ")

st.header("Select image")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 200px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 200px;
        margin-left: -200px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# sidebar
with st.sidebar:
    # Start button
    st.text("Click here to start")
    if st.button("Start"):
        st.experimental_rerun()

# upload image
text = "Click Browse files to upload an image"
image_file = st.file_uploader(text, type=["png","jpg","jpeg"])

# display image
try: 
    if image_file is not None:
        image = Image.open(image_file,  mode='r')
        _, mid, _ = st.columns([2,6,2])
        with mid:
            st.image(adjust_orientation(image), caption=image_file.name, width = 400)
except: st.error("This is not image file.")

# --------------------------
# Fill in some values
st.header("Fill in the values")

with st.form("fill_values", clear_on_submit=True):
    cols = st.columns(4)
    col_name = ["Hb (g/dL)", "Hct (%)", "MCV (fL)", "MCH (pg)"]
    hb = cols[0].text_input(col_name[0])
    hct = cols[1].text_input(col_name[1])
    mcv = cols[2].text_input(col_name[2])
    mch = cols[3].text_input(col_name[3])
    submitted = st.form_submit_button('Submit')

if submitted:
    try: 
        if hb != "" and hct != "" and mcv != "" and mch != "":
            if hb.isinstance() and hct.isinstance() and mcv.isinstance() and mch.isinstance():
                st.success("Filled completely!")
                values = {
                    "Hb": int(hb),
                    "Hct": int(hct),
                    "MCV": int(mcv),
                    "MCH": int(mch)
                }
                result = api(image, values)
            else: 
                st.error("Please enter numbers")
                result = None
        else: 
            st.error("Filled incompletely")
            result = None

        if values is not None:
            st.write(values)
    except: st.error("Please upload the image")

# update sidebar
if 'result' in locals():
    with st.sidebar:
        st.text("Export file")
        with io.BytesIO() as buffer:
        # Write the zip file to the buffer
            with zipfile.ZipFile(buffer, "w") as zip:
                zip.writestr("Data.json", json.dumps(result))

            buffer.seek(0)

            download = st.download_button(
                label="Export",
                data=buffer,  # Download buffer
                file_name="file.zip" 
                )


st.header("Result")
try:
    
    if result is not None: 
        st.write(result)

        
except: st.text("No image upload or fill values in the boxes")





