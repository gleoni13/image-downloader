import os
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. Configurazione del Browser
options = webdriver.ChromeOptions()
# Impostiamo una risoluzione fissa, larga e molto alta. 
# Questo forza Scribd a caricare le immagini ad alta qualità 
# e riduce i cambi di scala sballati.
options.add_argument("--window-size=1400,2000") 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://it.scribd.com/document/465353269/Brancalonia-Avventura-Luppoli"
driver.get(url)

print("Browser avviato.")
# È fondamentale chiudere il primissimo banner dei cookie a mano e assicurarsi 
# di aver fatto login (se necessario per vedere le pagine finali).
input("Risolvi eventuali banner o fai il login. Premi INVIO qui nel terminale quando il documento è pronto da scorrere...")

# 2. Pulizia radicale dell'interfaccia tramite JavaScript
print("Pulizia dell'interfaccia in corso...")
driver.execute_script("""
    // 1. Cerca e nascondi tutti gli elementi 'fissi' o 'incollati' allo schermo (Header, bottoni social, chat, banner)
    document.querySelectorAll('*').forEach(el => {
        let style = window.getComputedStyle(el);
        if (style.position === 'fixed' || style.position === 'sticky') {
            el.style.display = 'none';
        }
    });
    
    // 2. Nascondi selettori specifici di Scribd che fungono da intermezzo o disturbo
    let classi_disturbo = '.header_wrapper, .doc_info, .page_tools, .document_actions, .between_page_module, .related_docs, .doc_bottom_metadata';
    document.querySelectorAll(classi_disturbo).forEach(el => el.style.display = 'none');
""")

# 3. Identificazione delle pagine
pagine = driver.find_elements(By.CSS_SELECTOR, "div[data-page-number]")
if not pagine:
    pagine = driver.find_elements(By.CLASS_NAME, "outer_page")

print(f"Trovate {len(pagine)} pagine da elaborare.")
immagini_pagine = []

# 4. Ciclo di cattura (Adesso le foto non avranno overlay!)
for indice, pagina in enumerate(pagine):
    numero_pagina = indice + 1
    
    # Mette la pagina esattamente al centro della visuale
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pagina)
    time.sleep(3.5) # Pausa generosa per consentire al testo di caricarsi (Lazy Loading)
    
    nome_immagine = f"temp_pagina_{numero_pagina}.png"
    # Facciamo lo screenshot SOLO del div della pagina, che ora sarà pulito
    pagina.screenshot(nome_immagine)
    immagini_pagine.append(nome_immagine)
    
    print(f"Catturata pagina {numero_pagina}/{len(pagine)}")

# 5. Generazione del PDF con misure standardizzate
if immagini_pagine:
    print("Creazione del PDF in corso (Standardizzazione delle dimensioni)...")
    
    pagine_convertite = []
    
    # Apriamo la prima pagina e la usiamo come standard assoluto per altezza e larghezza
    prima_immagine = Image.open(immagini_pagine[0]).convert('RGB')
    larghezza_base, altezza_base = prima_immagine.size
    pagine_convertite.append(prima_immagine)
    
    # Processiamo tutte le altre
    for img_path in immagini_pagine[1:]:
        img = Image.open(img_path).convert('RGB')
        
        # Se le dimensioni differiscono anche di un solo pixel, riadattiamo l'immagine
        if img.size != (larghezza_base, altezza_base):
            img = img.resize((larghezza_base, altezza_base), Image.Resampling.LANCZOS)
            
        pagine_convertite.append(img)
        
    nome_pdf = "Brancalonia_X1_Pugno_Luppoli.pdf"
    
    # Salva fuso
    pagine_convertite[0].save(
        nome_pdf, 
        save_all=True, 
        append_images=pagine_convertite[1:]
    )
    print(f"Successo! File salvato come: {nome_pdf}")
    
    # Pulizia file temporanei
    for img in immagini_pagine:
        if os.path.exists(img):
            os.remove(img)
else:
    print("Errore: Non è stato possibile catturare alcuna pagina.")

driver.quit()