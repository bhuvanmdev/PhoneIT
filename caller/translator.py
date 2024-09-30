from IndicTrans2.huggingface_interface.models.main_functions import initialize_model_and_tokenizer,batch_translate
from IndicTrans2.huggingface_interface.IndicTransTokenizer.IndicTransTokenizer import IndicProcessor
import torch


#LANGUAGE CODES

# Assamese (asm_Beng)	Kashmiri (Arabic) (kas_Arab)	Punjabi (pan_Guru)
# Bengali (ben_Beng)	Kashmiri (Devanagari) (kas_Deva)	Sanskrit (san_Deva)
# Bodo (brx_Deva)	Maithili (mai_Deva)	Santali (sat_Olck)
# Dogri (doi_Deva)	Malayalam (mal_Mlym)	Sindhi (Arabic) (snd_Arab)
# English (eng_Latn)	Marathi (mar_Deva)	Sindhi (Devanagari) (snd_Deva)
# Konkani (gom_Deva)	Manipuri (Bengali) (mni_Beng)	Tamil (tam_Taml)
# Gujarati (guj_Gujr)	Manipuri (Meitei) (mni_Mtei)	Telugu (tel_Telu)
# Hindi (hin_Deva)	Nepali (npi_Deva)	Urdu (urd_Arab)
# Kannada (kan_Knda)	Odia (ory_Orya)	





# en_indic_ckpt_dir1 = "ai4bharat/indictrans2-en-indic-dist-200M"
# en_indic_tokenizer1, en_indic_model1 = initialize_model_and_tokenizer(en_indic_ckpt_dir1, "en-indic","4-bit",DEVICE=DEVICE)
# indic_en_ckpt_dir = "ai4bharat/indictrans2-indic-en-dist-200M"  # ai4bharat/indictrans2-indic-en-dist-200M
# indic_en_tokenizer, indic_en_model = initialize_model_and_tokenizer(indic_en_ckpt_dir, "indic-en", "4-bit",DEVICE=DEVICE)
class Translate:
    BATCH_SIZE=4
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    quantization = "4-bit"
    def __init__(self,en_indic_ckpt_dir,indic_en_ckpt_dir):
        self.en_indic_tokenizer1 ,self.en_indic_model1 = initialize_model_and_tokenizer(en_indic_ckpt_dir, "en-indic","4-bit",DEVICE=Translate.DEVICE)
        self.indic_en_tokenizer ,self.indic_en_model = initialize_model_and_tokenizer(indic_en_ckpt_dir, "indic-en", "4-bit",DEVICE=Translate.DEVICE)
        self.ip = IndicProcessor(inference=True)
    def translate(self,text,lang,op):

        langdic={"en-IN":"eng_Latn","hi-IN":"hin_Deva","kn-IN":"kan_Knda","bn-IN":"ben_Beng","ta-IN":"tam_Taml"}  
        if op: #english to anything op =1
            in_lang="eng_Latn"
            out_lang=langdic[lang]
            text_split=text.split(".")
            out=[]
            for i in text_split:
                if i!="":
                    out.append(i)
            return "".join(batch_translate(out, in_lang, out_lang, self.en_indic_model, self.en_indic_tokenizer, self.ip,BATCH_SIZE=Translate.BATCH_SIZE,DEVICE=Translate.DEVICE))
            
        else:
            in_lang=langdic[lang]
            out_lang="eng_Latn"
            if in_lang in ["hin_Deva","ben_Beng"]:
                text_split=text.split("।")
            else:
                text_split=text.split(".")
            out=[]
            for i in text_split:
                out.append(i)
            try:
                out.remove("")
            except:
                pass
            return "".join(batch_translate(out, in_lang, out_lang, self.indic_en_model, self.indic_en_tokenizer, self.ip,BATCH_SIZE=Translate.BATCH_SIZE,DEVICE=Translate.DEVICE))