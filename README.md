# 🔐 Web Password Generator (Python + Flask)

Ein moderner und leichter **Web-Passwort-Generator**, geschrieben in **Python** und **Flask**.  
Die Anwendung erzeugt sichere Passwörter direkt im Browser – mit auswählbarer Länge und individuellen Zeichentypen.
Developt by Markus Stuefer 


## 🐳 Docker

Die Anwendung kann einfach mit Docker gestartet werden:

```bash
# Docker Image bauen
docker build -t password-generator .

# Container starten
docker run -p 5000:5000 password-generator
```

Die Anwendung ist dann unter `http://localhost:5000` erreichbar.

---

Um es über Domain verfügbar zu machen braucht man ein revers proxy

Zum beispiel HAProxy Oder Nginx

