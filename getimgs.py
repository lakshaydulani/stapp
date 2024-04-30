import fitz
from PIL import Image
import io
import os

def save_images(filename = "samplereport.pdf"):
    output = []
    pdf_file = fitz.open(filename)
    
        #create folder named imgs if it doesnt exist
    if not os.path.exists("imgs"):
        os.mkdir("imgs")
    else:
        # clear all files inside folder "imgs"
        for f in os.listdir("imgs"):
            os.remove(os.path.join("imgs", f))
            
    
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.get_images()
        txt = page.get_text()
        # print(txt, image_list)
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            

        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.get_images(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            # save it to local disk
            image.save(open(f"imgs/image{page_index+1}_{image_index}.{image_ext}", "wb"))
            
if __name__ == "__main__":
    save_images("empirical.pdf")
            
            