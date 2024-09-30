from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

datas = collect_data_files('spacy', include_py_files=True)
hiddenimports = collect_submodules('spacy')

datas += copy_metadata('spacy')
datas += collect_data_files('spacy_pkuseg')
datas += collect_data_files('xx_ent_wiki_sm')
datas += collect_data_files('en_core_web_md')