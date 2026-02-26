.PHONY: jupyter pipeline streamlit zip clean

# Membuka Jupyter Notebook untuk menjalankan interaktif
jupyter:
	jupyter notebook

# Menjalankan LatentArt Pipeline Notebook secara otomatis (headless)
pipeline:
	jupyter nbconvert --execute --to notebook --inplace LatentArt_Pipeline_submission_BFGAI_Muhammad_Muqorrobin.ipynb

# Menjalankan Streamlit Notebook secara otomatis (headless)
# (Akan men-generate file logic.py dan menjalankan Streamlit di background)
streamlit:
	jupyter nbconvert --execute --to notebook --inplace LatentArt_Streamlit_submission_BFGAI_Muhammad_Muqorrobin.ipynb

# Membungkus proyek ke dalam satu file .zip untuk disubmit
zip:
	zip -r BFGAI_Muhammad_Muqorrobin.zip \
		LatentArt_Pipeline_submission_BFGAI_Muhammad_Muqorrobin.ipynb \
		LatentArt_Streamlit_submission_BFGAI_Muhammad_Muqorrobin.ipynb \
		requirements.txt \
		video_demo_aplikasi_BFGAI.mp4

# Membersihkan file autogenerate (.py, zip, dll)
clean:
	rm -f BFGAI_Muhammad_Muqorrobin.zip logic.py app.py
