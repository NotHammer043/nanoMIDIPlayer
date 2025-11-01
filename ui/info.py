import customtkinter as ctk
from tkinterweb import HtmlFrame
import markdown
import emoji
import re
import webbrowser
import urllib.request
import threading
import os
import logging
from modules.functions import mainFunctions

logger = logging.getLogger(__name__)

class InfoTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        logger.info("InfoTab initialized")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.htmlFrame = HtmlFrame(
            self,
            messages_enabled=False,
            on_link_click=self.openLink
        )
        self.htmlFrame.grid(row=0, column=0, sticky="nsew")
        self.__class__.htmlFrame = self.htmlFrame

        self.htmlFrame.load_html("<html><body><p style='color:white'>Loading info...</p></body></html>")
        logger.debug("Initial loading message displayed")

        self.after(100, self.startLoader)

    def startLoader(self):
        threading.Thread(target=self.loadContent, daemon=True).start()
        logger.debug("Started background thread for loadContent")

    def loadContent(self):
        mdContent = None
        try:
            logger.info("Attempting to fetch INFO.md from GitHub")
            with urllib.request.urlopen(
                "https://raw.githubusercontent.com/NotHammer043/nanoMIDIPlayer/refs/heads/main/api/INFO.md",
                timeout=5
            ) as response:
                mdContent = response.read().decode("utf-8")
                logger.info("Fetched INFO.md successfully")
        except Exception as e:
            logger.warning(f"Failed to fetch remote INFO.md: {e}")
            try:
                infoOffline = mainFunctions.resourcePath("assets/INFO-offline.md")
                with open(infoOffline, "r", encoding="utf-8") as f:
                    mdContent = f.read()
                    logger.info("Loaded offline INFO.md successfully")
            except FileNotFoundError:
                mdContent = "# Error\nINFO-offline.md not found remotely or locally."
                logger.error("INFO.md not found remotely or locally")

        def updateUI():
            try:
                htmlContent = markdown.markdown(
                    mdContent,
                    extensions=["extra", "toc", "tables", "fenced_code"]
                )

                def svgEmoji(char, *_):
                    codepoints = "-".join(f"{ord(c):x}" for c in char)
                    return f'<img src="https://twemoji.maxcdn.com/v/latest/svg/{codepoints}.svg" alt="{char}" width="20" height="20" style="vertical-align:middle;" />'

                htmlContent = emoji.replace_emoji(htmlContent, svgEmoji)
                htmlContent = re.sub(r'<!-- donator-table -->\s*<table>', '<table class="donator-table">', htmlContent)
                htmlContent = re.sub(r'<!-- beta-table -->\s*<table>', '<table class="beta-table">', htmlContent)

                htmlTemplate = f"""
                <html>
                    <head>
                        <style>
                            body {{
                                background-color: #0c0c0c;
                                color: white;
                                font-family: "Segoe UI Emoji", "Noto Color Emoji", "Apple Color Emoji", Arial, sans-serif;
                                padding: 20px;
                            }}
                            table {{
                                border-collapse: collapse;
                                margin: 10px auto;
                                max-width: 95%;
                                table-layout: fixed;
                                word-wrap: break-word;
                                overflow-wrap: break-word;
                            }}
                            th, td {{
                                padding: 5px;
                                text-align: left;
                                color: white;
                                border: 1px solid #00ff00;
                                white-space: normal;
                                word-break: break-word;
                            }}
                            th {{
                                background-color: #2e2e2e;
                                color: #00ff00;
                            }}
                            tr:nth-child(even) {{
                                background-color: #252525;
                            }}
                            img {{
                                max-width: 100%;
                                height: auto;
                            }}
                            pre, code {{
                                background: #2e2e2e;
                                padding: 5px;
                                border-radius: 5px;
                                color: white;
                            }}
                            h1, h2, h3, h4, h5 {{
                                color: #00ff00;
                                margin-top: 0;
                                margin-bottom: 0.5em;
                            }}
                            a {{
                                color: #00ff00;
                                text-decoration: none;
                            }}
                            .donator-table th, .donator-table td {{
                                border: 1px solid #00ff00;
                            }}
                            .donator-table th {{
                                color: #00ff00;
                            }}
                            .beta-table th, .beta-table td {{
                                border: 1px solid #a020f0;
                            }}
                            .beta-table th {{
                                color: #a020f0;
                            }}
                        </style>
                    </head>
                    <body>
                        {htmlContent}
                    </body>
                </html>
                """
                self.htmlFrame.load_html(htmlTemplate)
                logger.info("HTML content loaded into HtmlFrame")
            except Exception as e:
                logger.exception(f"Error processing markdown or HTML: {e}")

        self.after(0, updateUI)

    def openLink(self, url):
        logger.info(f"Opening link: {url}")
        webbrowser.open(url)
        return "break"
