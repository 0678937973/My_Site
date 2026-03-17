# This script creates clean HTML files without encoding issues

html_files = {
    'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mpho Dynal Mabena · IT Professional</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <span><strong>Mpho Dynal Mabena</strong></span> |
            <a href="{{ url_for('home') }}">Home</a> |
            <a href="{{ url_for('about') }}">About</a> |
            <a href="{{ url_for('contact') }}">Contact</a>
        </nav>
    </header>
    <main>
        <section>
            <p>
                Johannesburg, South Africa |
                <a href="mailto:mabenampho64@gmail.com">mabenampho64@gmail.com</a> |
                079 963 3750 / 067 893 7973 |
                <a href="https://www.linkedin.com/in/mabenampho54" target="_blank">linkedin.com/in/mabenampho54</a>
            </p>
        </section>
        <h1>Professional Summary</h1>
        <p>Detail-oriented Information Technology graduate with a Diploma in IT and hands-on experience in full-stack development, IT infrastructure support, and system administration. Proven ability to develop and deploy web applications using modern frameworks, manage Linux-based servers, and troubleshoot complex technical issues. Strong foundation in database design, API development, and security best practices. Committed to continuous learning and delivering high-quality results in collaborative technical environments.</p>
    </main>
    <footer>
        <p>© {{ current_year() }} Mpho Dynal Mabena. All rights reserved.</p>
    </footer>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>''',

    'about.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Me · Mpho Dynal Mabena</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <span><strong>Mpho Dynal Mabena</strong></span> |
            <a href="{{ url_for('home') }}">Home</a> |
            <a href="{{ url_for('about') }}">About</a> |
            <a href="{{ url_for('contact') }}">Contact</a>
        </nav>
    </header>
    <main>
        <section>
            <p>
                Johannesburg, South Africa |
                <a href="mailto:mabenampho64@gmail.com">mabenampho64@gmail.com</a> |
                079 963 3750 / 067 893 7973 |
                <a href="https://www.linkedin.com/in/mabenampho54" target="_blank">linkedin.com/in/mabenampho54</a>
            </p>
        </section>
        <h1>About Me</h1>
        <section>
            <h2>Who I Am</h2>
            <p>I'm Mpho Dynal Mabena, an IT professional based in Johannesburg, South Africa. My journey in technology began with a curiosity about how systems work together — from the code that powers web applications to the servers that host them. I believe in building solutions that are not only functional but also secure, maintainable, and user-friendly.</p>
        </section>
        <section>
            <h2>My Approach</h2>
            <p>I view technology as a tool to solve real-world problems. Whether I'm designing a database schema, troubleshooting a server issue, or developing a RESTful API, I focus on the bigger picture: how does this serve the end user? I'm drawn to full-stack development because it allows me to understand and contribute to every layer of an application — from the browser down to the operating system.</p>
        </section>
    </main>
    <footer>
        <p>© {{ current_year() }} Mpho Dynal Mabena. All rights reserved.</p>
    </footer>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>''',

    'contact.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Me · Mpho Dynal Mabena</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <span><strong>Mpho Dynal Mabena</strong></span> |
            <a href="{{ url_for('home') }}">Home</a> |
            <a href="{{ url_for('about') }}">About</a> |
            <a href="{{ url_for('contact') }}">Contact</a>
        </nav>
    </header>
    <main>
        <section>
            <p>
                Johannesburg, South Africa |
                <a href="mailto:mabenampho64@gmail.com">mabenampho64@gmail.com</a> |
                079 963 3750 / 067 893 7973 |
                <a href="https://www.linkedin.com/in/mabenampho54" target="_blank">linkedin.com/in/mabenampho54</a>
            </p>
        </section>
        <h1>Contact Me</h1>
        <form action="{{ url_for('submit_contact') }}" method="post" id="contact-form">
            <label for="name">Your Name *</label><br>
            <input type="text" id="name" name="name" required><br><br>
            <label for="email">Your Email *</label><br>
            <input type="email" id="email" name="email" required><br><br>
            <label for="subject">Subject *</label><br>
            <input type="text" id="subject" name="subject" required><br><br>
            <label for="message">Message *</label><br>
            <textarea id="message" name="message" rows="6" required></textarea><br><br>
            <button type="submit">Send Message</button>
        </form>
    </main>
    <footer>
        <p>© {{ current_year() }} Mpho Dynal Mabena. All rights reserved.</p>
    </footer>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>'''
}

import os

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# Write each file with proper UTF-8 encoding
for filename, content in html_files.items():
    filepath = os.path.join('templates', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {filepath}")

print("All HTML files created successfully!")