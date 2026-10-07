"""
Full content seeding for Django, React, Java, Python, and C.
Run: python manage.py seed_languages
"""
from django.core.management.base import BaseCommand
from apps.languages.models import Language
from apps.content.models import Section, Subsection, ContentItem


def code_item(title, code, language, analogy="", gotcha=""):
    return {"type": "code", "data": {"title": title, "code": code, "language": language, "analogy": analogy, "gotcha": gotcha}}

def note_item(text):
    return {"type": "note", "data": {"text": text}}

def heading_item(text):
    return {"type": "heading", "data": {"text": text}}

def para_item(text):
    return {"type": "paragraph", "data": {"text": text}}

def tip_item(text):
    return {"type": "tip", "data": {"text": text}}

def warning_item(text):
    return {"type": "warning", "data": {"text": text}}


LANGUAGES = [
    # ========================= PYTHON =========================
    {
        "name": "Python", "slug": "python",
        "description": "Python programming language - variables, loops, functions, OOP, file handling, and more",
        "display_order": 1, "status": "active",
        "sections": [
            {
                "title": "Python Basics", "slug": "python-basics",
                "description": "Fundamental concepts: output, input, variables, data types, operators",
                "subsections": [
                    {
                        "title": "Hello World & Output", "slug": "hello-world-output",
                        "items": [
                            code_item("Hello World & f-Strings", 'print("Hello, World!")\n\nname = "Shoaib"\nage = 24\nprint(name)\nprint(age)\n\n# f-Strings (formatted strings)\nprint(f"My name is {name}")', "python", "print() is like a megaphone - it announces your message to the world", "In Python 2, print was a statement: print 'hello'"),
                            note_item("Python uses print() to display output. f-Strings (formatted strings starting with f) are the modern way to embed variables in strings."),
                        ]
                    },
                    {
                        "title": "Taking User Input", "slug": "user-input",
                        "items": [
                            code_item("Getting Input", 'name = input("Enter your name: ")\nprint(name)\n\n# Integer input\nage = int(input("Enter age: "))\n\n# Float input\nsalary = float(input("Enter salary: "))', "python", "input() is like a question - Python waits for the user to respond", "input() always returns a string. Cast to int/float for numbers."),
                        ]
                    },
                    {
                        "title": "Variables & Data Types", "slug": "variables-data-types",
                        "items": [
                            code_item("Variables & Type Checking", 'name = "Shoaib"     # str\nage = 24            # int\ncgpa = 3.75         # float\nis_student = True   # bool\n\n# Check type\nprint(type(age))    # <class \'int\'>\nprint(type(name))   # <class \'str\'>', "python", "Variables are like labeled boxes - you put data in them and label what's inside"),
                            para_item("Python has dynamic typing - you don't need to declare variable types. The type is inferred from the value."),
                        ]
                    },
                    {
                        "title": "Comments & Escape Characters", "slug": "comments-escape",
                        "items": [
                            code_item("Comments & Escape Sequences", '# Single line comment\n\n"""\nMulti-line\ncomment (docstring)\n"""\n\n# Escape characters\nprint("Hello\\nWorld")   # New line\nprint("Hello\\tWorld")   # Tab\nprint("He said \\"Hi\\"") # Double quote', "python"),
                            tip_item("Use meaningful comments to explain WHY your code does something, not WHAT it does. The code itself shows what."),
                        ]
                    },
                    {
                        "title": "Operators", "slug": "operators",
                        "items": [
                            code_item("Arithmetic, Comparison & Logical", 'a = 10\nb = 3\n\n# Arithmetic\nprint(a + b)   # 13\nprint(a ** b)  # 1000 (power)\nprint(a // b)  # 3 (floor division)\nprint(a % b)   # 1 (modulus)\n\n# Comparison\nprint(a == b)  # False\nprint(a > b)   # True\n\n# Logical\nprint(a > 5 and b < 5)   # True\nprint(a > 5 or b > 5)    # True\nprint(not False)          # True', "python", "Operators are like Swiss Army knives - each one does a specific job on your data"),
                        ]
                    },
                    {
                        "title": "Strings Deep Dive", "slug": "strings-deep",
                        "items": [
                            code_item("String Methods & Slicing", 'name = "Python Programming"\n\n# Indexing & Slicing\nprint(name[0])       # P\nprint(name[-1])      # g\nprint(name[0:6])     # Python\nprint(name[7:])      # Programming\nprint(name[::-1])    # Reverse\n\n# Common methods\nprint(name.lower())\nprint(name.upper())\nprint(name.strip())\nprint(name.replace("P", "J"))\nprint(name.split())  # ["Python", "Programming"]\n\n# Check methods\nprint(name.isalpha())\nprint(name.startswith("Py"))', "python", "Strings are like necklaces - each character is a bead you can access by position"),
                        ]
                    },
                ]
            },
            {
                "title": "Control Flow", "slug": "control-flow",
                "description": "Conditional statements and loops",
                "subsections": [
                    {
                        "title": "if-elif-else Statements", "slug": "if-elif-else",
                        "items": [
                            code_item("Conditionals & Ternary", 'age = 18\n\nif age >= 18:\n    print("Adult")\nelif age >= 13:\n    print("Teen")\nelse:\n    print("Child")\n\n# Ternary operator (one-liner)\nstatus = "Adult" if age >= 18 else "Minor"\n\n# Nested conditions\nmarks = 85\nif marks >= 80:\n    print("A+")\nelif marks >= 70:\n    print("A")\nelse:\n    print("B")', "python", "if-else is like a choose-your-own-adventure book", "Python uses indentation (4 spaces) instead of braces {} for code blocks"),
                        ]
                    },
                    {
                        "title": "Loops & Iterations", "slug": "loops-iterations",
                        "items": [
                            code_item("For & While Loops", '# For loop with range\nfor i in range(5):\n    print(i)  # 0,1,2,3,4\n\n# range(start, stop, step)\nfor i in range(2, 10, 2):\n    print(i)  # 2,4,6,8\n\n# Iterate over list\nfruits = ["apple", "banana", "cherry"]\nfor fruit in fruits:\n    print(fruit)\n\n# While loop\ni = 0\nwhile i < 5:\n    print(i)\n    i += 1\n\n# Break and Continue\nfor i in range(10):\n    if i == 5:\n        break      # exit loop\n    if i % 2 == 0:\n        continue   # skip even\n    print(i)        # prints odd only', "python", "A loop is like a treadmill - keeps going until told to stop", "Infinite loops: while True without an exit condition. Always ensure loop variable changes."),
                        ]
                    },
                ]
            },
            {
                "title": "Data Structures", "slug": "data-structures",
                "description": "Lists, tuples, sets, dictionaries",
                "subsections": [
                    {
                        "title": "Lists & List Comprehensions", "slug": "lists",
                        "items": [
                            code_item("List Operations", 'numbers = [1, 2, 3, 4, 5]\nnumbers.append(6)      # add to end\nnumbers.insert(1, 100)  # insert at index\nnumbers.remove(3)       # remove value\nnumbers.pop()           # remove last\nnumbers.sort()          # sort in place\nnumbers.reverse()       # reverse\n\n# List comprehension\nsquares = [x*x for x in range(1, 6)]  # [1,4,9,16,25]\nevens = [x for x in range(10) if x % 2 == 0]', "python", "Lists are like shopping lists - ordered, changeable, allows duplicates"),
                        ]
                    },
                    {
                        "title": "Tuples, Sets & Dictionaries", "slug": "tuples-sets-dicts",
                        "items": [
                            code_item("Tuple, Set, Dict", '# Tuple (immutable)\ndata = (10, 20, 30)\nprint(data.count(20))  # 1\nprint(data.index(30))  # 2\n\n# Set (unique, unordered)\nnums = {1, 2, 3, 3}\nprint(nums)  # {1, 2, 3}\nnums.add(4)\nprint(nums.union({5, 6}))\n\n# Dictionary (key-value)\nstudent = {"name": "Shoaib", "age": 24}\nprint(student["name"])\nprint(student.keys())\nprint(student.values())\nprint(student.items())\nstudent["cgpa"] = 3.8  # add/update\nstudent.pop("age")     # remove', "python", "Dictionaries are like real dictionaries - look up a word (key) to get its meaning (value)"),
                            tip_item("Use a dictionary when you need key-value pairs. Use a set when you need unique elements. Use a tuple for immutable sequences."),
                        ]
                    },
                ]
            },
            {
                "title": "Functions", "slug": "functions",
                "description": "Function definitions, parameters, lambda, decorators",
                "subsections": [
                    {
                        "title": "Defining Functions", "slug": "defining-functions",
                        "items": [
                            code_item("Functions & Parameters", 'def greet(name="Guest"):\n    """Say hello."""  # docstring\n    return f"Hello, {name}!"\n\n# Lambda functions\nsquare = lambda x: x * x\nprint(square(5))  # 25\n\n# *args (multiple positional)\ndef sum_all(*numbers):\n    return sum(numbers)\n\n# **kwargs (keyword arguments)\ndef user_info(**details):\n    for key, val in details.items():\n        print(f"{key}: {val}")', "python", "A function is like a recipe - define once, reuse many times", "Default arguments are evaluated only ONCE at definition time, not each call."),
                        ]
                    },
                    {
                        "title": "Exception Handling", "slug": "exception-handling",
                        "items": [
                            code_item("Try-Except-Finally", 'try:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f"Error: {e}")\nexcept Exception as e:\n    print(f"General error: {e}")\nelse:\n    print("No error occurred")\nfinally:\n    print("Always runs - cleanup here")', "python", "try-except is like a safety net - catch errors before they crash your program"),
                        ]
                    },
                ]
            },
            {
                "title": "File Handling & OOP", "slug": "file-handling-oop",
                "description": "File operations and Object-Oriented Programming",
                "subsections": [
                    {
                        "title": "File Operations", "slug": "file-operations",
                        "items": [
                            code_item("Read & Write Files", '# Write file\nwith open("data.txt", "w") as f:\n    f.write("Hello World")\n\n# Read file\nwith open("data.txt", "r") as f:\n    content = f.read()\n    print(content)\n\n# Read lines\nwith open("data.txt", "r") as f:\n    for line in f.readlines():\n        print(line.strip())', "python", "with statement auto-closes the file - like a self-closing door", "File modes: r=read, w=write(overwrites), a=append, r+=read+write"),
                        ]
                    },
                    {
                        "title": "OOP - Classes & Inheritance", "slug": "oop-classes",
                        "items": [
                            code_item("Classes, Inheritance, Decorators", 'class Student:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n    def greet(self):\n        return f"Hi, I\'m {self.name}"\n\n# Inheritance\nclass Person:\n    def __init__(self, name):\n        self.name = name\n\nclass Student(Person):\n    def __init__(self, name, grade):\n        super().__init__(name)\n        self.grade = grade\n\n# Property decorator\nclass Circle:\n    def __init__(self, radius):\n        self._radius = radius\n\n    @property\n    def radius(self):\n        return self._radius\n\n    @radius.setter\n    def radius(self, value):\n        if value > 0:\n            self._radius = value', "python", "Classes are blueprints; objects are houses built from those blueprints"),
                        ]
                    },
                ]
            },
        ]
    },

    # ========================= DJANGO =========================
    {
        "name": "Django", "slug": "django",
        "description": "Django web framework - models, views, templates, ORM, admin, authentication",
        "display_order": 2, "status": "active",
        "sections": [
            {
                "title": "Getting Started", "slug": "django-getting-started",
                "description": "Installation, project creation, running the development server",
                "subsections": [
                    {
                        "title": "Install & Create Project", "slug": "install-create",
                        "items": [
                            code_item("Django Setup", '# Install Django\npip install django\n\n# Check version\ndjango-admin --version\n\n# Create project\ndjango-admin startproject myproject\n\n# Run server (default port 8000)\npython manage.py runserver\n\n# Custom port\npython manage.py runserver 8001\n\n# Create app\npython manage.py startapp blog', "python", "Django project = building; apps = individual rooms with specific purposes."),
                            note_item("Always register your apps in INSTALLED_APPS in settings.py after creating them. Each app handles a specific functionality."),
                        ]
                    },
                    {
                        "title": "Project Structure", "slug": "project-structure",
                        "items": [
                            code_item("Project Files", '# myproject/\n# ├── manage.py          # CLI tool\n# ├── myproject/\n# │   ├── settings.py    # Config\n# │   ├── urls.py        # URL routing\n# │   ├── asgi.py         # ASGI config\n# │   └── wsgi.py         # WSGI config\n# └── blog/                # Your app\n#     ├── admin.py        # Admin config\n#     ├── apps.py         # App config\n#     ├── models.py       # Database models\n#     ├── views.py        # View logic\n#     └── migrations/     # DB migrations', "python"),
                            para_item("manage.py is your Swiss Army knife - it handles migrations, server, shell, createsuperuser, and more."),
                        ]
                    },
                ]
            },
            {
                "title": "Models & Database", "slug": "django-models",
                "description": "Django ORM, models, migrations, and queries",
                "subsections": [
                    {
                        "title": "Creating Models", "slug": "creating-models",
                        "items": [
                            code_item("Django ORM Models", 'from django.db import models\n\nclass Post(models.Model):\n    title = models.CharField(max_length=100)\n    content = models.TextField()\n    created_at = models.DateTimeField(auto_now_add=True)\n    updated_at = models.DateTimeField(auto_now=True)\n\n    def __str__(self):\n        return self.title\n\n# Relationships\nclass Comment(models.Model):\n    post = models.ForeignKey(Post, on_delete=models.CASCADE)\n    text = models.TextField()\n\nclass Student(models.Model):\n    courses = models.ManyToManyField(Course)', "python", "Models are blueprints; migrations build the actual database tables.", "Always run 'makemigrations' then 'migrate' after model changes."),
                        ]
                    },
                    {
                        "title": "ORM Queries & Migrations", "slug": "orm-queries",
                        "items": [
                            code_item("Queries & Migrations", '# Create migrations\n# python manage.py makemigrations\n# python manage.py migrate\n# python manage.py showmigrations\n\n# CRUD Operations\nPost.objects.create(title="First Post")\nPost.objects.all()\nPost.objects.get(id=1)\nPost.objects.filter(title__contains="Python")\nPost.objects.filter(id__gt=5)\nPost.objects.filter(id__lt=10)\npost = Post.objects.get(id=1)\npost.title = "Updated"\npost.save()\npost.delete()', "python", "Django ORM is like a translator - you write Python, it writes SQL for you"),
                        ]
                    },
                ]
            },
            {
                "title": "Views & URL Routing", "slug": "django-views-urls",
                "description": "Function/class-based views, URL configuration",
                "subsections": [
                    {
                        "title": "URL Routing & Views", "slug": "url-routing",
                        "items": [
                            code_item("Views & URLs", 'from django.shortcuts import render\nfrom django.http import HttpResponse\nfrom django.urls import path, include\n\n# Function-based view\ndef home(request):\n    return render(request, "home.html", {"name": "Shoaib"})\n\n# URL pattern\nurlpatterns = [\n    path("", home, name="home"),\n    path("blog/", include("blog.urls")),\n]\n\n# Class-based views\nfrom django.views.generic import ListView, DetailView\n\nclass PostListView(ListView):\n    model = Post\n    template_name = "posts.html"\n\nclass PostDetailView(DetailView):\n    model = Post\n    template_name = "post_detail.html"', "python", "URLs are street addresses - Django routes requests to the correct view (house)."),
                        ]
                    },
                ]
            },
            {
                "title": "Templates & Forms", "slug": "django-templates-forms",
                "description": "Template rendering, form handling, CSRF",
                "subsections": [
                    {
                        "title": "Templates", "slug": "templates",
                        "items": [
                            code_item("Django Templates", '<!-- templates/home.html -->\n<h1>Hello {{ name }}</h1>\n\n{% if user.is_authenticated %}\n  <p>Welcome back!</p>\n{% endif %}\n\n{% for post in posts %}\n  <h2>{{ post.title }}</h2>\n  <p>{{ post.content }}</p>\n{% endfor %}\n\n<!-- Static files -->\n{% load static %}\n<link rel="stylesheet" href="{% static \'css/style.css\' %}">\n<img src="{% static \'images/logo.png\' %}" alt="Logo">', "django", "Templates are fill-in-the-blank forms - Django fills the blanks with real data"),
                        ]
                    },
                    {
                        "title": "Forms & ModelForms", "slug": "forms",
                        "items": [
                            code_item("Django Forms", 'from django import forms\nfrom django.forms import ModelForm\nfrom .models import Post\n\n# Regular form\nclass ContactForm(forms.Form):\n    name = forms.CharField(max_length=100)\n    email = forms.EmailField()\n    message = forms.CharField(widget=forms.Textarea)\n\n# ModelForm\nclass PostForm(ModelForm):\n    class Meta:\n        model = Post\n        fields = ["title", "content"]\n        # fields = "__all__"\n\n# Template\n# <form method="POST">\n#   {% csrf_token %}\n#   {{ form.as_p }}\n#   <button type="submit">Save</button>\n# </form>', "python", "ModelForms auto-generate form fields from your model - like a photocopier for database fields"),
                        ]
                    },
                ]
            },
            {
                "title": "Admin & Auth", "slug": "django-admin-auth",
                "description": "Django admin panel, user authentication, permissions",
                "subsections": [
                    {
                        "title": "Admin Panel & Auth", "slug": "admin-auth",
                        "items": [
                            code_item("Admin & Authentication", '# Create superuser\n# python manage.py createsuperuser\n\n# Register model in admin.py\nfrom django.contrib import admin\nfrom .models import Post\nadmin.site.register(Post)\n\n# Authentication\nfrom django.contrib.auth.models import User\nfrom django.contrib.auth import login, logout\nfrom django.contrib.auth.decorators import login_required\n\n# Create user\nUser.objects.create_user(username="john", password="12345")\n\n# Login required\ndef dashboard(request):\n    if request.user.is_authenticated:\n        pass  # user is logged in\n\n# Decorator\n@login_required\ndef profile(request):\n    return render(request, "profile.html")', "python", "Django admin is like a built-in CMS - fully functional backend out of the box"),
                        ]
                    },
                ]
            },
        ]
    },

    # ========================= REACT =========================
    {
        "name": "React", "slug": "react",
        "description": "React JS library - components, hooks, state, props, routing, and more",
        "display_order": 3, "status": "active",
        "sections": [
            {
                "title": "React Fundamentals", "slug": "react-fundamentals",
                "description": "JSX, components, props, state, event handling",
                "subsections": [
                    {
                        "title": "Components & JSX", "slug": "components-jsx",
                        "items": [
                            code_item("React Components", '// Functional Component\nfunction Welcome() {\n  return <h1>Hello React</h1>;\n}\n\n// Arrow Function Component\nconst User = ({ name, age }) => {\n  return (\n    <div>\n      <h2>{name}</h2>\n      <p>Age: {age}</p>\n    </div>\n  );\n};\n\n// JSX Rules\n// 1. Must return ONE parent element (use <>...</> fragment)\n// 2. Use className instead of class\n// 3. JavaScript in curly braces: {expression}\n\nconst element = (\n  <>\n    <h1>Title</h1>\n    <p>{2 + 2}</p>\n  </>\n);', "react", "Components are like LEGO blocks - build complex UIs by combining simple pieces", "JSX must have ONE root element. Use fragments (<>...</>) to wrap multiple elements."),
                        ]
                    },
                    {
                        "title": "useState Hook & Events", "slug": "usestate-events",
                        "items": [
                            code_item("State & Event Handling", 'import { useState } from "react";\n\nfunction Counter() {\n  const [count, setCount] = useState(0);\n  const [name, setName] = useState("");\n\n  const handleClick = () => {\n    setCount(prev => prev + 1); // functional update\n  };\n\n  return (\n    <>\n      <h1>Count: {count}</h1>\n      <button onClick={handleClick}>+1</button>\n      \n      <input\n        value={name}\n        onChange={(e) => setName(e.target.value)}\n        placeholder="Enter name"\n      />\n      <p>Hello {name}</p>\n    </>\n  );\n}', "react", "useState is like a sticky note - you can write and update values React remembers", "State updates are async! Use setCount(prev => prev + 1) when depending on previous state."),
                        ]
                    },
                    {
                        "title": "Conditional Rendering & Lists", "slug": "conditional-lists",
                        "items": [
                            code_item("Conditionals & Lists", '// Conditional Rendering\n{isLoggedIn ? <h1>Welcome</h1> : <h1>Please Login</h1>}\n\n{isAdmin && <AdminPanel />}  // short-circuit\n\n{isLoading ? (\n  <Loader />\n) : status === "error" ? (\n  <Error />\n) : (\n  <Content />\n)}\n\n// Lists & Keys\nconst users = ["Shoaib", "Ali", "Hasan"];\n\nreturn (\n  <ul>\n    {users.map((user, index) => (\n      <li key={index}>{user}</li>\n    ))}\n  </ul>\n);\n\n// With objects\n{posts.map(post => (\n  <div key={post.id}>\n    <h2>{post.title}</h2>\n    <p>{post.body}</p>\n  </div>\n))}', "react", "Conditional rendering is like traffic lights - show different UIs based on the state"),
                            warning_item("Always provide a unique 'key' prop when rendering lists. Index keys are okay for static lists but use unique IDs for dynamic data."),
                        ]
                    },
                ]
            },
            {
                "title": "React Hooks", "slug": "react-hooks",
                "description": "useEffect, useRef, useContext, custom hooks",
                "subsections": [
                    {
                        "title": "useEffect & Data Fetching", "slug": "useeffect",
                        "items": [
                            code_item("useEffect Hook", 'import { useState, useEffect } from "react";\n\nfunction Users() {\n  const [users, setUsers] = useState([]);\n  const [count, setCount] = useState(0);\n\n  // Run once on mount\n  useEffect(() => {\n    fetch("https://api.example.com/users")\n      .then(res => res.json())\n      .then(data => setUsers(data));\n  }, []);\n\n  // Run when count changes\n  useEffect(() => {\n    document.title = `Count: ${count}`;\n  }, [count]);\n\n  // With cleanup (unmount)\n  useEffect(() => {\n    const timer = setInterval(() => {\n      console.log("tick");\n    }, 1000);\n\n    return () => clearInterval(timer);\n  }, []);\n\n  return <div>{users.length} users</div>;\n}', "react", "useEffect is like a subscription - you set it up and clean it up when done", "Always include all dependencies in the array. Missing deps = stale closures."),
                        ]
                    },
                    {
                        "title": "useRef & useContext", "slug": "useref-usecontext",
                        "items": [
                            code_item("useRef & useContext", 'import { useRef, useContext, createContext } from "react";\n\n// useRef - access DOM elements\nfunction FocusInput() {\n  const inputRef = useRef(null);\n\n  const focusInput = () => {\n    inputRef.current?.focus();\n  };\n\n  return <input ref={inputRef} />;\n}\n\n// useContext - global state\nconst ThemeContext = createContext("light");\n\nfunction ThemedButton() {\n  const theme = useContext(ThemeContext);\n  return <button className={theme}>Click</button>;\n}\n\n// Provider wraps children\nfunction App() {\n  return (\n    <ThemeContext.Provider value="dark">\n      <ThemedButton />\n    </ThemeContext.Provider>\n  );\n}', "react", "Context is like a radio broadcast - one transmitter, many receivers. No prop drilling needed."),
                        ]
                    },
                    {
                        "title": "Custom Hooks", "slug": "custom-hooks",
                        "items": [
                            code_item("Creating Custom Hooks", '// Custom hook for counter logic\nfunction useCounter(initialValue = 0) {\n  const [count, setCount] = useState(initialValue);\n\n  const increment = () => setCount(c => c + 1);\n  const decrement = () => setCount(c => c - 1);\n  const reset = () => setCount(initialValue);\n\n  return { count, increment, decrement, reset };\n}\n\n// Using the custom hook\nfunction Counter() {\n  const { count, increment, decrement, reset } = useCounter(10);\n\n  return (\n    <>\n      <h1>{count}</h1>\n      <button onClick={increment}>+</button>\n      <button onClick={decrement}>-</button>\n      <button onClick={reset}>Reset</button>\n    </>\n  );\n}', "react", "Custom hooks = reusable stateful logic, like mixins but cleaner"),
                        ]
                    },
                ]
            },
            {
                "title": "React Router & API Calls", "slug": "react-router-api",
                "description": "Navigation, routing, and HTTP requests",
                "subsections": [
                    {
                        "title": "React Router", "slug": "react-router",
                        "items": [
                            code_item("Routing Setup", "npm install react-router-dom\n\n// App.jsx\nimport { BrowserRouter, Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';\n\nfunction App() {\n  return (\n    <BrowserRouter>\n      <nav>\n        <Link to=\"/\">Home</Link>\n        <Link to=\"/about\">About</Link>\n      </nav>\n      <Routes>\n        <Route path=\"/\" element={<Home />} />\n        <Route path=\"/about\" element={<About />} />\n        <Route path=\"/user/:id\" element={<User />} />\n        <Route path=\"*\" element={<NotFound />} />\n      </Routes>\n    </BrowserRouter>\n  );\n}\n\n// Inside a component\nconst navigate = useNavigate();\nconst { id } = useParams();  // get URL params\nnavigate('/dashboard');  // programmatic navigation", "react", "React Router is like a GPS - it shows different views based on the URL path"),
                        ]
                    },
                    {
                        "title": "API Calls with Axios", "slug": "api-axios",
                        "items": [
                            code_item("Fetch & Axios", "npm install axios\n\nimport axios from 'axios';\n\nfunction UserList() {\n  const [users, setUsers] = useState([]);\n\n  useEffect(() => {\n    // Using fetch\n    fetch('https://api.example.com/users')\n      .then(res => res.json())\n      .then(data => setUsers(data));\n\n    // Using axios (cleaner)\n    axios.get('https://api.example.com/users')\n      .then(res => setUsers(res.data));\n\n    // POST with axios\n    axios.post('/api/users', { name, email })\n      .then(res => console.log(res.data));\n\n    // Async/await\n    const fetchData = async () => {\n      const response = await axios.get('/api/posts');\n      setUsers(response.data);\n    };\n  }, []);\n}", "react", "Axios is like fetch() with superpowers - automatic JSON parsing, interceptors, better error handling"),
                        ]
                    },
                ]
            },
            {
                "title": "Styling & Performance", "slug": "styling-performance",
                "description": "CSS approaches, memoization, optimization",
                "subsections": [
                    {
                        "title": "Styling Components", "slug": "styling",
                        "items": [
                            code_item("CSS Approaches", '// Inline styles\n<h1 style={{ color: "red", fontSize: "24px" }}>Hello</h1>\n\n// External CSS\nimport "./App.css";\n\n// CSS Modules\nimport styles from "./App.module.css";\n<h1 className={styles.title}>Hello</h1>\n\n// className with conditions\n<button className={`btn ${isActive ? "active" : ""}`}>\n  Click\n</button>\n\n// Using clsx or classnames library\nimport clsx from "clsx";\n<button className={clsx("btn", { active: isActive })}>\n  Click\n</button>', "react"),
                        ]
                    },
                    {
                        "title": "Memoization", "slug": "memoization",
                        "items": [
                            code_item("React.memo, useMemo, useCallback", 'import { memo, useMemo, useCallback } from "react";\n\n// React.memo - skip re-render if props same\nconst User = memo(function User({ name }) {\n  return <h1>{name}</h1>;\n});\n\n// useMemo - cache expensive computation\nfunction ExpensiveList({ items, filter }) {\n  const filtered = useMemo(() => {\n    return items.filter(item => item.includes(filter));\n  }, [items, filter]); // recompute only when deps change\n\n  return filtered.map(item => <div key={item}>{item}</div>);\n}\n\n// useCallback - cache function reference\nfunction Parent() {\n  const handleClick = useCallback((id) => {\n    console.log("Clicked", id);\n  }, []); // stable reference across renders\n\n  return <Child onClick={handleClick} />;\n}', "react", "Memoization is like caching - don't recalculate what hasn't changed"),
                        ]
                    },
                ]
            },
        ]
    },

    # ========================= JAVA =========================
    {
        "name": "Java", "slug": "java",
        "description": "Java programming - OOP, classes, inheritance, collections, exception handling",
        "display_order": 4, "status": "active",
        "sections": [
            {
                "title": "Java Basics", "slug": "java-basics",
                "description": "Program structure, variables, data types, input/output, operators",
                "subsections": [
                    {
                        "title": "Program Structure & Variables", "slug": "program-variables",
                        "items": [
                            code_item("Java Basics", 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n\n        // Variables\n        int age = 24;\n        double salary = 25000.50;\n        char grade = \'A\';\n        boolean flag = true;\n\n        // Constants\n        final double PI = 3.14159;\n        static final int MAX_USERS = 100;\n\n        // Type casting\n        int num = 50;\n        double value = num;  // widening (auto)\n        int amount = (int) 45.9;  // narrowing (manual)\n    }\n}', "java", "Java's main() is like the front door - everything starts there", "Java is case-sensitive. String ≠ string."),
                        ]
                    },
                    {
                        "title": "Input & Data Types", "slug": "input-data-types",
                        "items": [
                            code_item("Scanner Input & Types", 'import java.util.Scanner;\n\nScanner sc = new Scanner(System.in);\n\n// Different input types\nString name = sc.nextLine();\nint age = sc.nextInt();\nfloat salary = sc.nextFloat();\ndouble value = sc.nextDouble();\nboolean status = sc.nextBoolean();\nchar ch = sc.next().charAt(0);\n\n// Data types sizes\n// byte (8-bit), short (16), int (32), long (64)\n// float (32), double (64), char (16), boolean\n\nlong big = 10000000000L;  // L suffix for long\nfloat pi = 3.14f;         // f suffix for float', "java"),
                        ]
                    },
                    {
                        "title": "Operators & Conditionals", "slug": "operators-conditionals",
                        "items": [
                            code_item("Ops, if-else, switch", '// Arithmetic: + - * / % ++ --\n// Comparison: == != > < >= <=\n// Logical: && || !\n// Assignment: = += -= *= /=\n\nint age = 18;\n\n// if-else-if\nif (age >= 18) {\n    System.out.println("Adult");\n} else if (age >= 13) {\n    System.out.println("Teen");\n} else {\n    System.out.println("Child");\n}\n\n// Ternary\nString result = (age >= 18) ? "Adult" : "Minor";\n\n// Switch\nswitch (day) {\n    case 1: System.out.println("Monday"); break;\n    case 2: System.out.println("Tuesday"); break;\n    default: System.out.println("Invalid");\n}', "java"),
                        ]
                    },
                ]
            },
            {
                "title": "Loops & Arrays", "slug": "java-loops-arrays",
                "description": "For, while, do-while loops, arrays, multi-dimensional arrays",
                "subsections": [
                    {
                        "title": "Loops", "slug": "loops",
                        "items": [
                            code_item("For, While, Do-While", '// For loop\nfor (int i = 0; i < 5; i++) {\n    System.out.println(i);\n}\n\n// Enhanced for (for-each)\nint[] nums = {1, 2, 3, 4, 5};\nfor (int num : nums) {\n    System.out.println(num);\n}\n\n// While loop\nint i = 0;\nwhile (i < 5) {\n    System.out.println(i);\n    i++;\n}\n\n// Do-while (runs at least once)\nint j = 0;\ndo {\n    System.out.println(j);\n    j++;\n} while (j < 5);\n\n// Control: break, continue', "java", "A loop is like a treadmill - it keeps going until you tell it to stop"),
                        ]
                    },
                    {
                        "title": "Arrays & Strings", "slug": "arrays-strings",
                        "items": [
                            code_item("Arrays, 2D Arrays, Strings", '// 1D Array\nint[] numbers = new int[5];\nint[] nums = {10, 20, 30, 40, 50};\nSystem.out.println(nums[0]);  // 10\nSystem.out.println(nums.length); // 5\n\n// 2D Array\nint[][] matrix = {\n    {1, 2, 3},\n    {4, 5, 6}\n};\nSystem.out.println(matrix[1][2]); // 6\n\n// Strings\nString name = "Java";\nname.length();\nname.toUpperCase();\nname.toLowerCase();\nname.trim();\nname.contains("Ja");\nname.indexOf("a");\nname.substring(0, 2);\nname.replace("J", "P");\nname.equals("Java");\nname.equalsIgnoreCase("java");', "java"),
                        ]
                    },
                ]
            },
            {
                "title": "Object-Oriented Programming", "slug": "java-oop",
                "description": "Classes, objects, constructors, inheritance, polymorphism, encapsulation, abstraction, interfaces",
                "subsections": [
                    {
                        "title": "Classes, Objects & Constructors", "slug": "classes-constructors",
                        "items": [
                            code_item("OOP - Classes", '// Class definition\nclass Student {\n    // Attributes\n    String name;\n    int age;\n\n    // Constructor\n    Student(String name, int age) {\n        this.name = name;\n        this.age = age;\n    }\n\n    // Method\n    void display() {\n        System.out.println(name + ": " + age);\n    }\n\n    // Getters & Setters (Encapsulation)\n    private double cgpa;\n    public double getCgpa() { return cgpa; }\n    public void setCgpa(double c) { this.cgpa = c; }\n}\n\n// Creating objects\nStudent s1 = new Student("Shoaib", 24);\ns1.display();', "java", "A class is a blueprint; an object is the house built from it"),
                        ]
                    },
                    {
                        "title": "Inheritance & Polymorphism", "slug": "inheritance-polymorphism",
                        "items": [
                            code_item("Inheritance, Polymorphism, Interfaces", '// Inheritance\nclass Person {\n    String name;\n    void eat() { System.out.println("Eating"); }\n}\n\nclass Student extends Person {\n    void study() { System.out.println("Studying"); }\n}\n\n// Polymorphism (method overriding)\nclass Animal {\n    void sound() { System.out.println("Animal sound"); }\n}\nclass Dog extends Animal {\n    @Override\n    void sound() { System.out.println("Bark"); }\n}\n\n// Abstract class\nabstract class Shape {\n    abstract void draw();\n}\n\n// Interface\ninterface Printable {\n    void print();\n}\nclass Document implements Printable {\n    public void print() { System.out.println("Printing..."); }\n}', "java", "Inheritance = family tree. Interfaces = contracts you must fulfill."),
                        ]
                    },
                ]
            },
            {
                "title": "Collections & Exception Handling", "slug": "java-collections",
                "description": "ArrayList, HashMap, HashSet, exception handling, file handling",
                "subsections": [
                    {
                        "title": "Collections Framework", "slug": "collections",
                        "items": [
                            code_item("ArrayList, HashSet, HashMap", 'import java.util.ArrayList;\nimport java.util.HashSet;\nimport java.util.HashMap;\n\n// ArrayList (dynamic array)\nArrayList<String> names = new ArrayList<>();\nnames.add("Java");\nnames.add("Python");\nnames.get(0);  // "Java"\nnames.remove(0);\nnames.size();\n\n// HashSet (unique elements)\nHashSet<Integer> nums = new HashSet<>();\nnums.add(1);\nnums.add(2);\nnums.add(1);  // duplicate, ignored\n\n// HashMap (key-value)\nHashMap<Integer, String> map = new HashMap<>();\nmap.put(1, "Java");\nmap.put(2, "Python");\nmap.get(1);  // "Java"', "java"),
                        ]
                    },
                    {
                        "title": "Exception Handling & Files", "slug": "exceptions-files",
                        "items": [
                            code_item("Try-Catch & File I/O", '// Exception handling\ntry {\n    int result = 10 / 0;\n} catch (ArithmeticException e) {\n    System.out.println("Cannot divide by zero");\n} catch (Exception e) {\n    System.out.println("General error");\n} finally {\n    System.out.println("Always executes");\n}\n\n// Throw custom exception\nthrow new Exception("Custom error");\n\n// File handling\nimport java.io.File;\nimport java.io.FileWriter;\nimport java.util.Scanner;\n\nFile file = new File("data.txt");\nFileWriter writer = new FileWriter("data.txt");\nwriter.write("Hello");\nwriter.close();\n\nScanner reader = new Scanner(file);\nwhile (reader.hasNextLine()) {\n    System.out.println(reader.nextLine());\n}', "java"),
                        ]
                    },
                ]
            },
        ]
    },

    # ========================= C =========================
    {
        "name": "C", "slug": "c",
        "description": "C programming - pointers, memory management, arrays, structures, file handling",
        "display_order": 5, "status": "active",
        "sections": [
            {
                "title": "C Fundamentals", "slug": "c-fundamentals",
                "description": "Program structure, variables, data types, input/output, operators",
                "subsections": [
                    {
                        "title": "Program Structure & I/O", "slug": "program-structure",
                        "items": [
                            code_item("C Basics", '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n\n    // Variables\n    int age = 20;\n    float pi = 3.14;\n    char grade = \'A\';\n\n    // Input\n    int num;\n    printf("Enter number: ");\n    scanf("%d", &num);\n    printf("You entered: %d\\n", num);\n\n    // Constants\n    const float PI = 3.14159;\n    #define MAX 100\n\n    // Format specifiers\n    // %d=int, %f=float, %c=char, %s=string, %lf=double\n    printf("Age: %d, Pi: %.2f\\n", age, pi);\n\n    return 0;\n}', "c", "C is like the assembly language of high-level languages - direct control over memory"),
                        ]
                    },
                    {
                        "title": "Operators & Conditionals", "slug": "operators-conditionals",
                        "items": [
                            code_item("Ops, if-else, switch", '#include <stdio.h>\n\nint main() {\n    int a = 10, b = 3;\n\n    // Arithmetic: + - * / %\n    printf("%d\\n", a + b);  // 13\n    printf("%d\\n", a % b);  // 1\n\n    // Comparison: == != > < >= <=\n    // Logical: && || !\n    // Increment: a++, ++a, a--, --a\n\n    int age = 18;\n    if (age >= 18) {\n        printf("Adult\\n");\n    } else if (age >= 13) {\n        printf("Teen\\n");\n    } else {\n        printf("Child\\n");\n    }\n\n    // Ternary\n    (age >= 18) ? printf("Adult\\n") : printf("Minor\\n");\n\n    // Switch\n    int choice = 2;\n    switch (choice) {\n        case 1: printf("One\\n"); break;\n        case 2: printf("Two\\n"); break;\n        default: printf("Invalid\\n");\n    }\n\n    return 0;\n}', "c"),
                        ]
                    },
                    {
                        "title": "Loops", "slug": "loops",
                        "items": [
                            code_item("For, While, Do-While", '#include <stdio.h>\n\nint main() {\n    // For loop\n    for (int i = 0; i < 5; i++) {\n        printf("%d\\n", i);\n    }\n\n    // While loop\n    int j = 0;\n    while (j < 5) {\n        printf("%d\\n", j);\n        j++;\n    }\n\n    // Do-while\n    int k = 0;\n    do {\n        printf("%d\\n", k);\n        k++;\n    } while (k < 5);\n\n    // Jump: break, continue, goto\n    for (int i = 0; i < 10; i++) {\n        if (i == 5) break;      // exit\n        if (i % 2 == 0) continue; // skip even\n        printf("%d\\n", i);\n    }\n\n    return 0;\n}', "c"),
                        ]
                    },
                ]
            },
            {
                "title": "Arrays & Strings", "slug": "c-arrays-strings",
                "description": "1D/2D arrays, string handling, string functions",
                "subsections": [
                    {
                        "title": "Arrays", "slug": "arrays",
                        "items": [
                            code_item("1D & 2D Arrays", '#include <stdio.h>\n\nint main() {\n    // 1D Array\n    int arr[5] = {10, 20, 30, 40, 50};\n    printf("%d\\n", arr[0]);\n\n    // Traverse\n    for (int i = 0; i < 5; i++) {\n        printf("%d ", arr[i]);\n    }\n\n    // 2D Array\n    int matrix[2][3] = {\n        {1, 2, 3},\n        {4, 5, 6}\n    };\n    printf("%d\\n", matrix[1][2]); // 6\n\n    // Matrix traversal\n    for (int i = 0; i < 2; i++) {\n        for (int j = 0; j < 3; j++) {\n            printf("%d ", matrix[i][j]);\n        }\n        printf("\\n");\n    }\n\n    return 0;\n}', "c"),
                        ]
                    },
                    {
                        "title": "Strings", "slug": "strings",
                        "items": [
                            code_item("String Functions", '#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char name[] = "Shoaib";\n    char dest[50];\n\n    printf("Length: %d\\n", strlen(name));  // 6\n    strcpy(dest, name);      // copy\n    strcat(dest, " Khan");   // concatenate\n    printf("%s\\n", dest);    // "Shoaib Khan"\n\n    // Comparison\n    if (strcmp(name, "Shoaib") == 0) {\n        printf("Same\\n");\n    }\n\n    // Find character\n    char *ptr = strchr(name, \'a\');\n\n    // Substring search\n    char *found = strstr(dest, "Khan");\n\n    // Input string\n    scanf("%s", name);  // no & needed for strings\n\n    return 0;\n}', "c", "C strings are character arrays ending with \\0 (null character)"),
                        ]
                    },
                ]
            },
            {
                "title": "Functions & Recursion", "slug": "c-functions",
                "description": "Function definition, parameters, recursion",
                "subsections": [
                    {
                        "title": "Functions", "slug": "functions",
                        "items": [
                            code_item("Functions & Recursion", '#include <stdio.h>\n\n// Function declaration (prototype)\nint add(int, int);\nvoid greet();\n\n// Function definition\nint add(int a, int b) {\n    return a + b;\n}\n\nvoid greet() {\n    printf("Hello!\\n");\n}\n\n// Recursion - factorial\nint factorial(int n) {\n    if (n == 0) return 1;   // base case\n    return n * factorial(n - 1); // recursive case\n}\n\nint main() {\n    int sum = add(5, 3);     // 8\n    printf("5! = %d\\n", factorial(5)); // 120\n    greet();\n    return 0;\n}', "c", "Recursion = a function calling itself. Always need a base case to stop!", "Infinite recursion causes stack overflow. Always ensure base case is reachable."),
                        ]
                    },
                ]
            },
            {
                "title": "Pointers & Memory", "slug": "c-pointers-memory",
                "description": "Pointers, dynamic memory allocation, malloc, calloc, free",
                "subsections": [
                    {
                        "title": "Pointers", "slug": "pointers",
                        "items": [
                            code_item("Pointers Deep Dive", '#include <stdio.h>\n\nint main() {\n    int num = 10;\n    int *ptr = &num;    // & = address of\n\n    printf("Value: %d\\n", num);    // 10\n    printf("Address: %p\\n", &num); // memory address\n    printf("Pointer: %p\\n", ptr);  // same address\n    printf("Dereferenced: %d\\n", *ptr); // 10 (value at address)\n\n    // Pointer arithmetic\n    int arr[] = {10, 20, 30};\n    int *p = arr;\n    printf("%d\\n", *p);     // 10\n    printf("%d\\n", *(p+1)); // 20\n\n    // NULL pointer\n    int *nullPtr = NULL;\n\n    // Double pointer\n    int **ptr2 = &ptr;\n\n    return 0;\n}', "c", "A pointer = a home address. It tells you WHERE something lives in memory", "Dereferencing NULL causes segmentation fault. Always check if(ptr != NULL)."),
                        ]
                    },
                    {
                        "title": "Dynamic Memory Allocation", "slug": "dynamic-memory",
                        "items": [
                            code_item("malloc, calloc, realloc, free", '#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    // malloc - allocate memory\n    int *arr;\n    arr = (int*) malloc(5 * sizeof(int));\n    if (arr == NULL) {\n        printf("Memory allocation failed\\n");\n        return 1;\n    }\n    arr[0] = 10;\n    arr[1] = 20;\n\n    // calloc - allocate + initialize to zero\n    int *arr2 = (int*) calloc(5, sizeof(int));\n\n    // realloc - resize\n    arr = realloc(arr, 10 * sizeof(int));\n\n    // Always free when done!\n    free(arr);\n    free(arr2);\n    arr = NULL;\n\n    return 0;\n}', "c", "malloc = renting memory. free = returning it. Never forget to return!", "Always free() malloc/calloc memory. Memory leaks crash long-running programs."),
                        ]
                    },
                ]
            },
            {
                "title": "Structures & File Handling", "slug": "c-structures-files",
                "description": "Structures, unions, enums, file operations",
                "subsections": [
                    {
                        "title": "Structures & Unions", "slug": "structures",
                        "items": [
                            code_item("Struct, Union, Enum", '#include <stdio.h>\n\n// Structure\nstruct Student {\n    int id;\n    char name[50];\n    float cgpa;\n};\n\n// Union (shares memory)\nunion Data {\n    int i;\n    float f;\n    char str[20];\n};\n\n// Enum\nenum Day {\n    SUN, MON, TUE, WED, THU, FRI, SAT\n};\n\nint main() {\n    struct Student s1 = {101, "Shoaib", 3.75};\n    printf("ID: %d, Name: %s\\n", s1.id, s1.name);\n\n    union Data d;\n    d.i = 10;\n    printf("%d\\n", d.i);\n\n    enum Day today = MON;\n    printf("Day: %d\\n", today); // 1\n\n    return 0;\n}', "c", "Structs group related data. Unions save memory by sharing space. Enums make code readable."),
                        ]
                    },
                    {
                        "title": "File Handling", "slug": "file-handling",
                        "items": [
                            code_item("Read & Write Files", '#include <stdio.h>\n\nint main() {\n    FILE *fp;\n\n    // Write to file\n    fp = fopen("data.txt", "w");\n    if (fp == NULL) {\n        printf("Error opening file\\n");\n        return 1;\n    }\n    fprintf(fp, "Hello World\\n");\n    fclose(fp);\n\n    // Read from file\n    fp = fopen("data.txt", "r");\n    char buffer[100];\n    while (fgets(buffer, 100, fp) != NULL) {\n        printf("%s", buffer);\n    }\n    fclose(fp);\n\n    // File modes: r=read, w=write, a=append,\n    // r+=r/w, w+=r/w, a+=append+r\n\n    return 0;\n}', "c", "File handling = opening a book (fopen), reading/writing (fprintf/fgets), closing (fclose)", "Always check if fopen() returns NULL. Always fclose() when done to prevent data loss."),
                        ]
                    },
                ]
            },
        ]
    },
]


class Command(BaseCommand):
    help = "Seed database with Django, React, Java, Python, C cheat sheet content"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding languages...\n")
        total_subsections = 0

        for lang_data in LANGUAGES:
            language, created = Language.objects.get_or_create(
                slug=lang_data["slug"],
                defaults={k: lang_data[k] for k in ["name", "description", "display_order", "status"]}
            )
            if not created:
                for k in ["name", "description", "display_order", "status"]:
                    setattr(language, k, lang_data[k])
                language.save()

            self.stdout.write(f"\n{'Created' if created else 'Updated'}: {language.name}")

            for sec_idx, sec_data in enumerate(lang_data.get("sections", [])):
                section, _ = Section.objects.get_or_create(
                    language=language, slug=sec_data["slug"],
                    defaults={"title": sec_data["title"], "description": sec_data.get("description", ""),
                              "display_order": sec_idx, "status": "active"}
                )
                section_lang_subs = 0

                for sub_idx, sub_data in enumerate(sec_data.get("subsections", [])):
                    subsection, _ = Subsection.objects.get_or_create(
                        section=section, slug=sub_data["slug"],
                        defaults={"title": sub_data["title"], "description": sub_data.get("description", ""),
                                  "display_order": sub_idx, "status": "active"}
                    )
                    # Replace content items
                    subsection.content_items.all().delete()
                    for idx, item_data in enumerate(sub_data.get("items", [])):
                        ContentItem.objects.create(
                            subsection=subsection, type=item_data["type"],
                            data=item_data["data"], display_order=idx, status="active"
                        )
                    section_lang_subs += 1
                    total_subsections += 1

                self.stdout.write(f"  ├─ {section.title} ({section_lang_subs} subsections)")

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Done! 5 languages, {total_subsections} subsections with code/content items created."
        ))