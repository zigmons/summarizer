import threading
import pyperclip
import rumps
import sys

from app.ia import get_chat_client
from app.settings import get_api_key, save_api_key
from google.genai import types

# Puxa a chave que já esteja salva
API_KEY = get_api_key()
print(f"[DEBUG] API_KEY carregada: {API_KEY}", file=sys.stderr)
client = get_chat_client(API_KEY) if API_KEY else None
print(f"[DEBUG] client instanciado: {client}", file=sys.stderr)


class SummarizerApp(rumps.App):

    def __init__(self):
        super().__init__(
            name="✂️ Summarizer",
            icon="resources/icon.png",
            menu=[
                "Resumir Clipboard",
                "Configurar API Key",
                None,
                "Sair"
            ]
        )
        # onde guardamos o resultado pendente
        self.pending_summary = None
        print("[DEBUG] App iniciado", file=sys.stderr)

    @rumps.clicked("Configurar API Key")
    def configure(self, _):
        print("[DEBUG] Clicou em Configurar API Key", file=sys.stderr)
        window = rumps.Window(
            title="Configurar API Key",
            message="Insira sua API Key:",
            default_text=get_api_key() or "",
            ok="Salvar",
            cancel="Cancelar"
        )
        res = window.run()
        print(f"[DEBUG] Window result: clicked={res.clicked}, text={res.text!r}", file=sys.stderr)
        if res.clicked and res.text.strip():
            key = res.text.strip()
            save_api_key(key)
            rumps.notification("Summarizer", "", "API Key salva com sucesso!")
            global client
            client = get_chat_client(key)
            print(f"[DEBUG] Novo client instanciado: {client}", file=sys.stderr)
        elif res.clicked:
            rumps.notification("Summarizer", "", "Chave vazia; nada salvo.")

    @rumps.clicked("Resumir Clipboard")
    def summarize(self, _):
        print("[DEBUG] Clicou em Resumir Clipboard", file=sys.stderr)
        if client is None:
            print("[DEBUG] client é None", file=sys.stderr)
            rumps.notification("Summarizer", "", "API Key não configurada!")
            return

        text = pyperclip.paste().strip()
        print(f"[DEBUG] Clipboard: {text!r}", file=sys.stderr)
        if not text:
            print("[DEBUG] Clipboard vazio", file=sys.stderr)
            rumps.notification("Summarizer", "", "Clipboard vazio.")
            return

        rumps.notification("Summarizer", "", "Gerando resumo…")
        print("[DEBUG] Iniciando thread de resumo", file=sys.stderr)

        def do_summary():
            print("[DEBUG] Thread do_summary entrou", file=sys.stderr)
            try:
                resp = client.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=text,
                    config=types.GenerateContentConfig(
                        max_output_tokens=256,
                        temperature=0.2
                    )
                )
                resumo = resp.text.strip()
                print(f"[DEBUG] Resposta da API: {resumo!r}", file=sys.stderr)
            except Exception as e:
                resumo = f"Erro ao chamar API: {e}"
                print(f"[DEBUG] Exceção na API: {e}", file=sys.stderr)
            # armazena para exibir no thread principal
            self.pending_summary = (text, resumo)
            print("[DEBUG] pending_summary setado", file=sys.stderr)

        threading.Thread(target=do_summary, daemon=True).start()

    @rumps.timer(0.5)
    def _show_summary(self, _):
        if self.pending_summary:
            original, resumo = self.pending_summary
            print("[DEBUG] Timer detectou pending_summary!", file=sys.stderr)
            # exibe a janela de resumo no main thread
            rumps.alert(f"Resumo de: {original[:20]}...", resumo)
            print("[DEBUG] Alert exibido", file=sys.stderr)
            self.pending_summary = None

    @rumps.clicked("Sair")
    def quit_app(self, _):
        print("[DEBUG] Saindo da aplicação", file=sys.stderr)
        rumps.quit()


if __name__ == "__main__":
    print("[DEBUG] Chamando SummarizerApp().run()", file=sys.stderr)
    SummarizerApp().run()
