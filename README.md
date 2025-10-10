# Dashboard App

A minimal and efficient productivity dashboard built with **Flask**, **Tailwind CSS**, **HTMX**, and **Alpine.js**. It includes task management, news updates, notes, scheduling, reminders, and theme customization.
.
## Features

* 📰 News via RSS feeds
* ✅ Task and to-do management
* 📝 Markdown note access
* 📅 Event scheduling with notes
* ⏰ Email-based reminders
* 🌙 Light/Dark mode toggle

## Tech Stack

* **Backend:** Flask, SQLite, Python libraries (`feedparser`, `markdown`, `smtplib`, `openpyxl`)
* **Frontend:** Tailwind CSS, HTMX, Alpine.js, JavaScript

## Setup

```bash
git clone https://github.com/your-username/dashboard-app.git
cd dashboard-app
pip install -r requirements.txt
python app.py
```

Visit: `http://localhost:5000`

## Tailwind Setup

```bash
npm install -D tailwindcss
npx tailwindcss init
```

In `tailwind.config.js`:

```js
module.exports = {
  content: ["./templates/**/*.html", "./static/**/*.js"],
  theme: { extend: {} },
  plugins: [],
}
```

In `static/input.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Build CSS:

```bash
npx tailwindcss -i ./static/input.css -o ./static/output.css --watch
```

## License

MIT License — see [LICENSE](LICENSE) for details.

