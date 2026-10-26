"""
Full content seeding for Django, React, Java, Python, and C.
Run: python manage.py seed_languages
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
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


C_CHEAT_SHEET = [
    ("Introduction to C", "What Is C?;History of C;Why Learn C?;Features of C;Applications of C;Advantages of C;Limitations of C;How C Works;The Compilation Process;Your First C Program"),
    ("Basic C Syntax", "Structure of a C Program;The main() Function;Header Files;Statements and Expressions;Code Blocks;Semicolons;Comments;C Tokens;C Keywords;Identifiers;Naming Conventions"),
    ("Variables and Constants", "What Is a Variable?;Variable Declaration;Variable Initialization;Variable Assignment;Variable Naming Rules;Local Variables;Global Variables;Scope of Variables;Lifetime of Variables;Constants Using const;Symbolic Constants;Numeric and Character Literals"),
    ("Data Types", "Overview of C Data Types;Integer Type: int;Character Type: char;Floating-Point Type: float;Double-Precision Type: double;Extended Precision: long double;Void Type: void;Short Integer: short;Long Integer: long;Long Long Integer: long long;Signed and Unsigned Types;The sizeof Operator;Format Specifiers;Boolean Values and <stdbool.h>;Type Sizes and Portability"),
    ("Input and Output", "Standard Input and Output;The printf() Function;The scanf() Function;Format Specifiers;Escape Sequences;Reading Characters with getchar();Writing Characters with putchar();Reading Strings with fgets();Displaying Strings with puts();Formatted Input and Output;Buffering Basics;The History and Removal of gets();Input Validation;Common Input/Output Mistakes"),
    ("Control Flow", "Control Flow Overview;Sequence, Selection, and Iteration;Flowcharts and Pseudocode;Tracing Program Execution;Truth Values in C;Common Control-Flow Mistakes"),
    ("Operators", "Introduction to Operators;Arithmetic Operators;Assignment Operators;Relational Operators;Logical Operators;Unary Operators;Increment and Decrement Operators;Bitwise Operators;Conditional (Ternary) Operator;Comma Operator;The sizeof Operator;Operator Precedence;Operator Associativity;Short-Circuit Evaluation;Common Operator Mistakes"),
    ("Type Conversion", "Introduction to Type Conversion;Implicit Type Conversion;Integer Promotions;Usual Arithmetic Conversions;Explicit Type Conversion;Type Casting;Conversion Between Integer and Floating-Point Types;Character and Integer Conversion;Signed and Unsigned Conversion;Narrowing and Precision Loss;Integer Division;Common Type Conversion Errors"),
    ("Decision Making", "Introduction to Decision Making;The if Statement;The if-else Statement;Nested if Statements;The else-if Ladder;The switch Statement;The default Case;The break Statement in switch;Nested Decision Structures;The Conditional (Ternary) Operator;Choosing Between if-else and switch;Common Decision-Making Mistakes"),
    ("Loops", "Introduction to Loops;The for Loop;The while Loop;The do-while Loop;Nested Loops;Infinite Loops;The break Statement;The continue Statement;The goto Statement;Loop Control Variables;Counter-Controlled Loops;Sentinel-Controlled Loops;Loop Tracing;Common Loop Mistakes"),
    ("Functions", "Introduction to Functions;Benefits of Functions;Function Declaration and Prototypes;Function Definition;Function Calls;Parameters and Arguments;Return Values;The void Return Type;Passing Arguments by Value;Simulating Reference-Based Modification with Pointers;Local and Global Variables;Recursive Functions;Base Cases and Recursive Cases;Function Scope and Lifetime;Standard Library Functions;Common Function Mistakes"),
    ("Arrays", "Introduction to Arrays;Declaring Arrays;Initializing Arrays;Accessing Array Elements;Traversing Arrays;Updating Array Elements;One-Dimensional Arrays;Two-Dimensional Arrays;Multidimensional Arrays;Arrays and Functions;Passing Arrays to Functions;Array Length Calculation;Searching Arrays;Sorting Arrays;Copying Arrays;Variable-Length Arrays;Array Bounds and Out-of-Bounds Access;Common Array Mistakes"),
    ("Strings", "Introduction to Strings in C;Character Arrays;The Null Terminator '\\0';Declaring and Initializing Strings;Reading Strings Safely;Displaying Strings;The strlen() Function;The strcpy() and strncpy() Functions;The strcat() and strncat() Functions;The strcmp() and strncmp() Functions;The strchr() and strrchr() Functions;The strstr() Function;The strtok() Function;Converting Strings to Numbers;Manual String Manipulation;Arrays of Strings;String Literals and Modifiable Arrays;Buffer Overflow Prevention;Common String Mistakes"),
    ("Pointers", "Introduction to Pointers;Declaring Pointer Variables;The Address-of Operator &;The Dereference Operator *;Pointer Initialization;Null Pointers;Void Pointers;Pointer Arithmetic;Pointers and Arrays;Pointers and Strings;Pointers to Pointers;Passing Pointers to Functions;Modifying Values Through Pointers;Function Pointers;Pointers to Arrays;Pointers to Structures;Const and Pointers;Dangling Pointers;Wild Pointers;Invalid Pointer Access;Common Pointer Mistakes"),
    ("Structures", "Introduction to Structures;Defining a Structure;Declaring Structure Variables;Initializing Structures;Accessing Structure Members;Designated Initializers;Nested Structures;Arrays of Structures;Pointers to Structures;The Arrow Operator ->;Passing Structures to Functions;Returning Structures from Functions;Structure Assignment;The typedef Keyword with Structures;Structure Padding and Alignment;Common Structure Mistakes"),
    ("Union", "Introduction to Unions;Defining a Union;Declaring Union Variables;Initializing Unions;Accessing Union Members;Union Memory Layout;Union Size and Alignment;Structures vs. Unions;Unions with Structures;Tagged Unions;Safe Union Usage;Common Union Mistakes"),
    ("Enumeration", "Introduction to Enumerations;Defining an enum;Declaring Enumeration Variables;Default Enumeration Values;Assigning Explicit Values;Duplicate Enumeration Values;Using Enums with switch;Enums and Readability;Enum Constants and Scope;Enumerations in Structures;Enumerations in Modern C;Common Enumeration Mistakes"),
    ("File Handling", "Introduction to File Handling;File Pointers;Opening Files with fopen();Closing Files with fclose();File Opening Modes;Writing Text with fprintf();Reading Formatted Data with fscanf();Writing Strings with fputs();Reading Lines with fgets();Character-Based File I/O;Writing Data with fwrite();Reading Data with fread();Binary Files;File Positioning with fseek();Getting File Position with ftell();Rewinding Files with rewind();Detecting End-of-File;Checking File Errors;File Existence and Error Handling;Safe File Handling Practices;Common File Handling Mistakes"),
    ("Dynamic Memory", "Introduction to Dynamic Memory Allocation;Stack vs. Heap Concepts;The malloc() Function;The calloc() Function;The realloc() Function;The free() Function;Checking Allocation Failures;Allocating Arrays Dynamically;Dynamic Strings;Dynamic Structures;Resizing Dynamic Arrays;Memory Ownership;Memory Leaks;Double Free Errors;Use-After-Free Errors;Dangling Pointers;Safe Memory Management Patterns;Common Dynamic Memory Mistakes"),
    ("Storage Classes", "Introduction to Storage Classes;Automatic Storage Duration;The auto Keyword;The register Keyword;The static Keyword;Static Local Variables;Static File-Scope Variables;The extern Keyword;External Linkage;Internal Linkage;Scope vs. Linkage vs. Storage Duration;Storage-Class Examples;Common Storage-Class Mistakes"),
    ("Preprocessor", "Introduction to the C Preprocessor;Preprocessing Directives;The #include Directive;The #define Directive;The #undef Directive;Conditional Compilation;The #if Directive;The #ifdef and #ifndef Directives;The #elif and #else Directives;The #endif Directive;The #error Directive;The #pragma Directive;The __FILE__ Macro;The __LINE__ Macro;The __DATE__ and __TIME__ Macros;Compiler-Dependent Preprocessor Features;Common Preprocessor Mistakes"),
    ("Macros", "Introduction to Macros;Object-Like Macros;Function-Like Macros;Macro Parameters;Parenthesizing Macro Arguments;Multiple Evaluation Hazards;Multi-Statement Macros;The do { ... } while (0) Pattern;Stringification Operator #;Token-Pasting Operator ##;Variadic Macros;Predefined Macros;Macros vs. Functions;Macros vs. Constants;Debugging Macros;Common Macro Mistakes"),
    ("Header Files", "Introduction to Header Files;Standard Header Files;User-Defined Header Files;Creating a Custom Header;Header File Organization;Header Guards;The #pragma once Directive;Declarations vs. Definitions;Function Prototypes in Headers;Sharing Types and Constants;Including Headers Correctly;Source Files and Header Files;Multiple Source File Projects;Compiling Multiple C Files;Avoiding Multiple-Definition Errors;Common Header File Mistakes"),
    ("Command-Line Arguments", "Introduction to Command-Line Arguments;The main() Function with argc and argv;Understanding argc;Understanding argv;Reading Command-Line Arguments;Converting Arguments to Integers;Converting Arguments to Floating-Point Values;Validating Command-Line Input;Handling Missing Arguments;Handling Extra Arguments;Command-Line Flags and Options;Returning Exit Status Codes;Example: Command-Line Calculator;Common Command-Line Argument Mistakes"),
    ("Bitwise Programming", "Introduction to Bits and Bytes;Binary Number Representation;Bitwise AND &;Bitwise OR |;Bitwise XOR ^;Bitwise NOT ~;Left Shift <<;Right Shift >>;Setting a Bit;Clearing a Bit;Toggling a Bit;Checking a Bit;Bit Masks;Bit Fields;Bitwise vs. Logical Operators;Signed Integer and Shift Considerations;Practical Bitwise Examples;Common Bitwise Programming Mistakes"),
    ("Error Handling", "Introduction to Error Handling;Syntax Errors;Compile-Time Errors;Linker Errors;Runtime Errors;Logical Errors;The errno Variable;The perror() Function;The strerror() Function;Return Codes;Error Codes and Enumerations;The assert() Macro;Input Validation;File Operation Errors;Memory Allocation Errors;Defensive Programming;Debugging with Compiler Warnings;Common Error-Handling Mistakes"),
    ("Standard Libraries", "Overview of the C Standard Library;<stdio.h> — Input and Output;<stdlib.h> — Utilities and Memory;<string.h> — String and Memory Operations;<math.h> — Mathematical Functions;<time.h> — Time and Date;<ctype.h> — Character Classification;<stdbool.h> — Boolean Support;<stdint.h> — Fixed-Width Integer Types;<inttypes.h> — Integer Formatting and Conversion;<limits.h> — Integer Limits;<float.h> — Floating-Point Limits;<stddef.h> — Common Definitions;<assert.h> — Assertions;<errno.h> — Error Reporting;<signal.h> — Signal Handling;<setjmp.h> — Nonlocal Jumps;<stdarg.h> — Variable Argument Lists;<locale.h> — Localization;<wchar.h> and <wctype.h> — Wide Characters;Standard Library Portability"),
    ("Math Library", "Introduction to <math.h>;The sqrt() Function;The pow() Function;Absolute Value Functions;The ceil() Function;The floor() Function;The round() Family;The fmod() Function;The remainder() Function;Exponential Functions;Logarithmic Functions;Trigonometric Functions;Inverse Trigonometric Functions;Hyperbolic Functions;Floating-Point Comparisons;Handling Domain and Range Errors;Compiling with the Math Library;Practical Mathematical Programs;Common Math Library Mistakes"),
    ("Time and Date", "Introduction to <time.h>;The time_t Type;The time() Function;The clock() Function;The difftime() Function;The struct tm Structure;The localtime() Function;The gmtime() Function;The mktime() Function;Formatting Dates with strftime();Converting Time with asctime() and ctime();Measuring CPU Time;Calendar Date Calculations;Time Zones and Portability;Practical Time and Date Programs;Common Time Handling Mistakes"),
    ("Character Library", "Introduction to <ctype.h>;The isalpha() Function;The isdigit() Function;The isalnum() Function;The islower() and isupper() Functions;The isspace() Function;The ispunct() Function;The isxdigit() Function;The isprint() and isgraph() Functions;The iscntrl() Function;The tolower() Function;The toupper() Function;Correct Use of Character Functions;Character Classification Programs;Locale Considerations;Common Character Handling Mistakes"),
    ("Memory Functions", "Introduction to Memory Operations;The memcpy() Function;The memmove() Function;The memset() Function;The memcmp() Function;The memchr() Function;memcpy() vs. memmove();Copying Memory Safely;Initializing Memory;Comparing Raw Memory;Searching Memory Blocks;Overlapping Memory Regions;Memory Bounds and Buffer Sizes;Practical Memory Function Programs;Common Memory Function Mistakes"),
    ("Searching Algorithms", "Introduction to Searching;Linear Search;Linear Search Algorithm;Linear Search Implementation;Binary Search;Binary Search Prerequisites;Iterative Binary Search;Recursive Binary Search;Searching Strings;Searching Structures;Time and Space Complexity;Best, Average, and Worst Cases;Linear Search vs. Binary Search;Practical Searching Programs;Common Searching Algorithm Mistakes"),
    ("Sorting Algorithms", "Introduction to Sorting;Bubble Sort;Selection Sort;Insertion Sort;Merge Sort;Quick Sort;Counting Sort Concepts;Sorting in Ascending Order;Sorting in Descending Order;Sorting Strings;Sorting Structures with qsort();The qsort() Function;Stable vs. Unstable Sorting;In-Place vs. Out-of-Place Sorting;Time and Space Complexity;Comparing Sorting Algorithms;Practical Sorting Programs;Common Sorting Algorithm Mistakes"),
    ("Practice Programs", "Hello World;Display Personal Information;Sum of Two Numbers;Swap Two Variables;Calculate Rectangle Area;Celsius to Fahrenheit Conversion;Simple Calculator;Even or Odd Number;Positive, Negative, or Zero;Find the Largest of Three Numbers;Leap Year Checker;Multiplication Table;Sum of Natural Numbers;Factorial of a Number;Fibonacci Series;Prime Number Checker;Prime Numbers in a Range;Armstrong Number Checker;Palindrome Number Checker;Reverse a Number;Sum of Digits;Count Digits;Greatest Common Divisor;Least Common Multiple;Power Calculation;Decimal-to-Binary Conversion;Array Sum and Average;Find Minimum and Maximum in an Array;Linear Search;Binary Search;Bubble Sort;Matrix Addition;Matrix Multiplication;Matrix Transpose;String Length Without strlen();Reverse a String;String Palindrome Checker;Count Vowels and Consonants;Count Words in a String;Student Marks and Grade Calculator;File Copy Program;File-Based Record Storage;Dynamic Array Example;Structure-Based Student Records"),
    ("Mini Projects", "Project 1: Console Calculator;Project 2: Student Record Management System;Project 3: Library Management System;Project 4: Contact Management System;Project 5: Bank Account Management System;Project 6: Inventory Management System;Project 7: Employee Payroll System;Project 8: Quiz Application;Project 9: Number Guessing Game;Project 10: Tic-Tac-Toe;Project 11: ATM Simulation;Project 12: Expense Tracker;Project 13: File-Based Login System;Project 14: Text File Analyzer;Project 15: Command-Line To-Do List;Project Planning and Requirements;Program Architecture and Function Design;Data Structures for Mini Projects;File Storage and Data Persistence;Input Validation and Error Handling;Testing and Debugging;Project Documentation;Suggested Extensions and Challenges"),
    ("Interview Questions", "Basic C Interview Questions;C History and Features;Compilation and Linking;Keywords and Identifiers;Variables and Data Types;printf() and scanf();Operators and Precedence;Decision-Making Statements;Loops and Loop Control;Functions and Recursion;Arrays and Strings;Pointers and Pointer Arithmetic;Null, Void, and Dangling Pointers;Structures and Unions;Enumerations and Typedef;Storage Classes and Linkage;Preprocessor and Macros;Dynamic Memory Allocation;File Handling;Bitwise Operations;Standard Library Functions;Undefined, Unspecified, and Implementation-Defined Behavior;Output Prediction Questions;Find-the-Bug Questions;Coding Interview Problems;Advanced C Interview Questions"),
    ("Best Practices", "Writing Readable C Code;Meaningful Naming Conventions;Consistent Formatting and Indentation;Using Functions Effectively;Avoiding Unnecessary Global Variables;Choosing Appropriate Data Types;Initializing Variables;Using const Correctly;Validating User Input;Checking Function Return Values;Safe String Handling;Pointer Safety;Dynamic Memory Management;File Handling Best Practices;Error Handling Strategies;Header and Source File Organization;Compiler Warnings;Portable C Programming;Writing Maintainable Code;Testing and Debugging;Documentation and Comments;Security-Aware C Programming;Performance and Optimization;Code Review Checklist"),
    ("Common Errors and Debugging", "Syntax Errors;Missing Semicolons;Misspelled Identifiers;Incorrect Header Files;Type Mismatch Errors;Format Specifier Errors;Uninitialized Variables;Incorrect Conditions;Infinite Loops;Off-by-One Errors;Array Out-of-Bounds Access;String Buffer Overflow;Missing Null Terminators;Incorrect Pointer Usage;Null Pointer Dereferencing;Dangling Pointers;Memory Leaks;Double Free Errors;Incorrect Dynamic Allocation Sizes;File Opening Failures;Incorrect File Modes;Division by Zero;Integer Overflow Considerations;Undefined Behavior;Compiler Warnings;Debugging with printf();Debugging with GDB;Using AddressSanitizer;Using UndefinedBehaviorSanitizer;Troubleshooting Compilation and Linking;Debugging Checklist"),
    ("C Keywords and Operator Precedence", "Complete C Keyword Reference;C90 Keywords;C99 Keywords;C11 Keywords;C17 Notes;C23 Keyword and Language Updates;Keywords vs. Identifiers;Reserved Identifiers;Complete Operator Reference;Operator Precedence Table;Operator Associativity;Unary Operators;Arithmetic Operators;Shift Operators;Relational Operators;Equality Operators;Bitwise Operators;Logical Operators;Conditional Operator;Assignment Operators;Comma Operator;Parentheses and Expression Grouping;Evaluation Order vs. Operator Precedence;Side Effects and Sequence Points;Common Precedence Traps;Output Prediction Examples"),
    ("Complete C Quick Reference", "Basic Program Template;Compilation Commands;Common Header Files;Common Data Types;Integer Type Modifiers;Format Specifier Reference;Escape Sequence Reference;Variable Declaration Syntax;Constants and Literals;Operators Quick Reference;Decision-Making Syntax;Loop Syntax;Function Syntax;Array Syntax;String Function Reference;Pointer Syntax;Structure Syntax;Union Syntax;Enumeration Syntax;Dynamic Memory Function Reference;File Handling Function Reference;Preprocessor Directive Reference;Macro Syntax;Standard Library Reference;Math Function Reference;Time and Date Function Reference;Character Function Reference;Memory Function Reference;Searching Algorithm Reference;Sorting Algorithm Reference;Common Error Codes and Diagnostics;Compiler Warning Checklist;Portable C Programming Checklist;Memory Safety Checklist;C Standards Compatibility Notes;Common Interview Revision Notes;Essential C Programming Patterns;Final C Programming Checklist"),
]


PYTHON_CHEAT_SHEET = [
    ("Introduction to Python", "What Is Python?;History of Python;Why Learn Python?;Features of Python;Applications of Python;Advantages of Python;Limitations of Python;Python vs. C;Python vs. Java;Python vs. JavaScript;Python Implementations: CPython, PyPy, and Others;How Python Executes Code;Interpreted and Compiled Execution;Python Versions and Compatibility;Your First Python Program"),
    ("Getting Started with Python", "Installing Python 3;Choosing a Python Version;Checking the Python Installation;The Python Interpreter;Using the Interactive Shell;Running a Python Script;Creating a .py File;Using an IDE or Code Editor;Using the VS Code Python Extension;Running Code from a Terminal;The Python REPL;Exiting the Interpreter;Using help() and dir();Choosing a Working Directory;Your First Script;Common Setup Problems"),
    ("Basic Python Syntax", "Structure of a Python Program;Python Statements;Expressions;Indentation;Code Blocks;Comments;Single-Line Comments;Docstrings;Identifiers;Naming Conventions;Python Keywords;Case Sensitivity;Line Continuation;Multiple Statements;Blank Lines and Readability;The pass Statement;The ... Ellipsis;The if __name__ == \"__main__\": Pattern;Common Syntax Errors"),
    ("Variables and Constants", "What Is a Variable?;Creating Variables;Variable Assignment;Multiple Variable Assignment;Assigning Multiple Values;Variable Reassignment;Dynamic Typing;Variable Naming Rules;Local Variables;Global Variables;Nonlocal Variables;Variable Scope;The global Keyword;The nonlocal Keyword;Constants by Convention;Module-Level Constants;Naming Constants with Uppercase Letters;Object Identity and the id() Function;Variable References;Mutable and Immutable Objects;Deleting Names with del;Common Variable Mistakes"),
    ("Python Data Types", "Introduction to Python Data Types;The type() Function;Numeric Types;Integers: int;Floating-Point Numbers: float;Complex Numbers: complex;Boolean Type: bool;Strings: str;Lists: list;Tuples: tuple;Ranges: range;Dictionaries: dict;Sets: set;Frozen Sets: frozenset;Binary Types: bytes;Mutable Byte Arrays: bytearray;Memory Views: memoryview;The NoneType and None;Mutable vs. Immutable Types;Checking Types with type() and isinstance();Type Annotations;Common Data Type Mistakes"),
    ("Input and Output", "Introduction to Input and Output;The print() Function;The input() Function;Reading User Input;Converting Input to Integers;Converting Input to Floating-Point Numbers;Reading Multiple Values;The sep Parameter;The end Parameter;Output Redirection with file;The flush Parameter;Formatted Strings with f-Strings;The format() Method;The format() Function;String Formatting with %;Numeric Formatting;Decimal Precision;Alignment and Padding;Reading Multiline Input;Handling Invalid Input;Common Input/Output Mistakes"),
    ("Operators", "Introduction to Operators;Arithmetic Operators;Addition, Subtraction, Multiplication, and Division;Floor Division;Modulus Operator;Exponentiation Operator;Assignment Operators;Comparison Operators;Equality and Identity;Logical Operators: and, or, and not;Membership Operators: in and not in;Identity Operators: is and is not;Bitwise Operators;Unary Operators;Augmented Assignment;Operator Precedence;Operator Associativity;Short-Circuit Evaluation;Chained Comparisons;Truthy and Falsy Values;Common Operator Mistakes"),
    ("Type Conversion", "Introduction to Type Conversion;Implicit Type Conversion;Explicit Type Conversion;Converting to int;Converting to float;Converting to complex;Converting to str;Converting to bool;Converting to list;Converting to tuple;Converting to set;Converting to dict;Converting Between Strings and Numbers;Converting Numeric Strings;Parsing Integers with a Base;Type Conversion vs. Type Casting;Handling ValueError;Precision Loss in Numeric Conversion;Floating-Point Representation;Common Type Conversion Mistakes"),
    ("Decision Making", "Introduction to Decision Making;The if Statement;The if-else Statement;The if-elif-else Chain;Nested if Statements;Multiple Conditions;Logical Conditions;Comparison Expressions;Truthy and Falsy Conditions;Conditional Expressions;The Ternary Expression;Nested Conditional Expressions;Pattern Matching with match-case;Guards in Pattern Matching;The pass Statement in Conditional Blocks;Choosing Between if and match;Common Decision-Making Mistakes"),
    ("Loops", "Introduction to Loops;The for Loop;The while Loop;Iterating Over Strings;Iterating Over Lists and Tuples;Iterating Over Dictionaries;The range() Function;The enumerate() Function;The zip() Function;Nested Loops;The break Statement;The continue Statement;The pass Statement;Loop else Clauses;Infinite Loops;Loop Control Variables;Iteration and Iterators;List Comprehensions;Nested Comprehensions;Generator Expressions;Common Loop Mistakes"),
    ("Functions", "Introduction to Functions;Defining a Function;Calling a Function;Function Parameters and Arguments;Positional Arguments;Keyword Arguments;Default Parameters;Required Parameters;Variable-Length Positional Arguments: *args;Variable-Length Keyword Arguments: **kwargs;Return Values;Returning Multiple Values;Functions Without an Explicit Return;Local and Global Scope;The global Keyword;The nonlocal Keyword;Recursive Functions;Lambda Functions;Higher-Order Functions;Functions as First-Class Objects;Passing Functions as Arguments;Returning Functions;Function Annotations;Docstrings;Positional-Only Parameters;Keyword-Only Parameters;Parameter Unpacking;Mutable Default Argument Pitfalls;Common Function Mistakes"),
    ("Lists and Tuples", "Introduction to Lists;Creating Lists;Accessing List Elements;Positive and Negative Indexing;List Slicing;Updating List Elements;Adding Elements with append();Adding Multiple Elements with extend();Inserting Elements with insert();Removing Elements with remove();Removing Elements with pop();Clearing Lists with clear();Searching Lists with index();Counting Elements with count();Sorting Lists with sort();Sorting with sorted();Reversing Lists;Copying Lists;Shallow Copies and Aliasing;Nested Lists;List Comprehensions;Lists as Stacks;Lists as Queues;List Unpacking;Introduction to Tuples;Creating Tuples;Accessing Tuple Elements;Tuple Packing and Unpacking;Single-Element Tuples;Tuple Immutability;Named Tuples;Lists vs. Tuples;Common List and Tuple Mistakes"),
    ("Strings", "Introduction to Strings;Creating Strings;Single, Double, and Triple Quotes;String Immutability;String Indexing;String Slicing;String Concatenation;String Repetition;String Membership;String Length with len();Changing Letter Case;upper() and lower();capitalize() and title();swapcase();Removing Whitespace with strip();lstrip() and rstrip();Searching with find() and index();Counting Substrings;Replacing Text with replace();Splitting Strings with split();Joining Strings with join();Prefix and Suffix Checks;String Testing Methods;String Formatting with f-Strings;Escape Sequences;Raw Strings;Unicode and Encoding;Encoding with encode();Decoding Bytes;Reversing Strings;Checking Palindromes;String Comparison;Regular Expressions Introduction;Common String Mistakes"),
    ("Dictionaries and Sets", "Introduction to Dictionaries;Creating Dictionaries;Accessing Dictionary Values;Adding and Updating Key-Value Pairs;Removing Items with pop();Removing Items with popitem();Deleting Items with del;Clearing Dictionaries;Dictionary Keys and Hashability;Dictionary Views;keys(), values(), and items();The get() Method;The setdefault() Method;The update() Method;Dictionary Merging;Dictionary Comprehensions;Nested Dictionaries;Iterating Through Dictionaries;Dictionary Unpacking;Introduction to Sets;Creating Sets;Adding Elements with add();Updating Sets;Removing Elements with remove() and discard();Clearing Sets;Set Union;Set Intersection;Set Difference;Symmetric Difference;Subsets and Supersets;Frozen Sets;Set Comprehensions;Practical Uses of Sets;Dictionaries vs. Lists;Sets vs. Lists;Common Dictionary and Set Mistakes"),
    ("Object-Oriented Programming", "Introduction to OOP;Classes and Objects;Defining a Class;Creating Objects;The __init__() Method;The self Parameter;Instance Attributes;Class Attributes;Instance Methods;Class Methods;Static Methods;Encapsulation;Public, Protected, and Private Naming Conventions;Name Mangling;Inheritance;Single Inheritance;Multiple Inheritance;Multilevel Inheritance;Hierarchical Inheritance;Method Overriding;The super() Function;Polymorphism;Duck Typing;Abstraction;Abstract Base Classes;Properties and the property() Decorator;Getters and Setters;Composition;Aggregation;Operator Overloading;Special Methods and Dunder Methods;__str__() and __repr__();__eq__() and Comparison Methods;Dataclasses;Class Design Best Practices;Common OOP Mistakes"),
    ("Exception Handling", "Introduction to Exceptions;Syntax Errors vs. Exceptions;The try Statement;The except Clause;Handling Specific Exceptions;Handling Multiple Exceptions;The else Clause;The finally Clause;Raising Exceptions with raise;Re-Raising Exceptions;Creating Custom Exceptions;Exception Chaining;The assert Statement;Common Built-in Exceptions;ValueError;TypeError;IndexError;KeyError;NameError;AttributeError;ZeroDivisionError;FileNotFoundError;ImportError and ModuleNotFoundError;OSError;Exception Hierarchy;Context Managers and Exception Safety;Logging Exceptions;EAFP vs. LBYL;Best Practices for Exception Handling;Common Exception Handling Mistakes"),
    ("Modules and Packages", "Introduction to Modules;What Is a Module?;Importing Modules;The import Statement;The from ... import Statement;Import Aliases with as;Importing Specific Names;The dir() Function;The help() Function;Built-in Modules;User-Defined Modules;Creating a Custom Module;Module Search Paths;The sys.path List;The __name__ Variable;The Main Guard;Introduction to Packages;Creating a Python Package;The __init__.py File;Absolute Imports;Relative Imports;Package Organization;Circular Imports;Installing Third-Party Packages;Understanding pip;Requirements Files;Package Version Constraints;Virtual Environments;Common Import Errors"),
    ("File Handling", "Introduction to File Handling;Opening Files with open();The with Statement;Reading Files with read();Reading Lines with readline();Reading All Lines with readlines();Iterating Over File Objects;Writing Files with write();Writing Multiple Lines with writelines();File Opening Modes;Text vs. Binary Modes;Appending to Files;File Encoding;UTF-8 Text Handling;File Pointers and Seeking;tell() and seek();Flushing and Closing Files;File and Directory Paths;The pathlib Module;Checking File Existence;Creating Directories;Renaming and Deleting Files;Copying Files;Temporary Files;Reading and Writing CSV Files;Reading and Writing JSON Files;Working with File Metadata;Handling File Exceptions;Safe File Operations;Common File Handling Mistakes"),
    ("Comprehensions, Iterators, and Generators", "Introduction to Comprehensions;List Comprehensions;Conditional List Comprehensions;Nested List Comprehensions;Dictionary Comprehensions;Set Comprehensions;Generator Expressions;Introduction to Iterables;Introduction to Iterators;The iter() Function;The next() Function;The Iterator Protocol;Creating a Custom Iterator;Introduction to Generators;Generator Functions;The yield Keyword;Generator State;yield from;Generator Expressions vs. List Comprehensions;Lazy Evaluation;Memory Efficiency;Generator Pipelines;Sending Values to Generators;Closing Generators;Common Iterator and Generator Mistakes"),
    ("Decorators and Closures", "Introduction to Decorators;Functions as Objects;Nested Functions;Returning Functions;Closures;Lexical Scope;The nonlocal Keyword;Creating a Simple Decorator;The @decorator Syntax;Wrapping Functions;Preserving Metadata with functools.wraps;Decorators with Arguments;Decorators on Methods;Class Decorators;Stacking Decorators;Parameterized Decorators;Timing Decorators;Logging Decorators;Authentication and Authorization Decorators;Built-in Decorators;@staticmethod;@classmethod;@property;Common Decorator Mistakes"),
    ("Functional Programming", "Introduction to Functional Programming;Pure Functions;Side Effects;First-Class Functions;Higher-Order Functions;Lambda Expressions;The map() Function;The filter() Function;The reduce() Function;The functools Module;Function Composition;Immutable Data Patterns;List Comprehensions vs. map();Filtering Collections;Transforming Collections;Sorting with Key Functions;The operator Module;Partial Functions;functools.partial();Caching with functools.cache;Memoization;Recursive Functional Patterns;Itertools Overview;Practical Functional Programming Examples;Common Functional Programming Mistakes"),
    ("Regular Expressions", "Introduction to Regular Expressions;The re Module;Raw String Patterns;Literal Characters;Metacharacters;Character Classes;Character Ranges;The Dot Metacharacter;Anchors: ^ and $;Quantifiers;Greedy and Non-Greedy Matching;Groups and Capturing Groups;Non-Capturing Groups;Alternation;Lookahead and Lookbehind;The re.match() Function;The re.search() Function;The re.fullmatch() Function;The re.findall() Function;The re.finditer() Function;The re.sub() Function;The re.split() Function;Compiling Patterns;Flags and Options;Email Pattern Limitations;Input Validation with Regular Expressions;Common Regex Mistakes"),
    ("Standard Library Essentials", "Overview of the Python Standard Library;The math Module;The statistics Module;The random Module;The secrets Module;The datetime Module;The time Module;The calendar Module;The os Module;The sys Module;The pathlib Module;The shutil Module;The glob Module;The re Module;The collections Module;Counter;defaultdict;deque;namedtuple;The itertools Module;The functools Module;The operator Module;The decimal Module;The fractions Module;The uuid Module;The enum Module;The pprint Module;The textwrap Module;The difflib Module;The typing Module;The dataclasses Module;Choosing the Right Standard Library Tool"),
    ("Date and Time", "Introduction to Date and Time;The datetime Module;The date Class;The time Class;The datetime Class;The timedelta Class;Creating Dates and Times;Getting the Current Date and Time;Formatting Dates with strftime();Parsing Dates with strptime();Date Arithmetic;Comparing Dates;Time Zones;Naive vs. Aware Datetimes;UTC and Local Time;The zoneinfo Module;Daylight Saving Time Considerations;Timestamps;Converting Timestamps;Measuring Execution Time;Calendar Generation;Practical Date and Time Programs;Common Date and Time Mistakes"),
    ("Working with Data Formats", "Introduction to Structured Data;JSON Basics;Reading JSON with json.load();Parsing JSON Strings with json.loads();Writing JSON with json.dump();Serializing with json.dumps();JSON Formatting and Indentation;Handling JSON Errors;CSV Basics;Reading CSV Files;Writing CSV Files;Using DictReader;Using DictWriter;Handling CSV Delimiters and Quotes;XML Basics;Reading XML with xml.etree.ElementTree;Writing XML;YAML Overview and Third-Party Support;TOML Basics;Reading TOML with tomllib;Serialization and Deserialization;Pickle Basics and Security Risks;Choosing a Data Format;Common Data Format Mistakes"),
    ("Working with the Operating System", "Introduction to OS Interaction;The os Module;The sys Module;Environment Variables;Reading Environment Variables;Working with Paths;The pathlib Module;Listing Directory Contents;Creating and Removing Directories;File and Directory Metadata;Renaming and Moving Files;Copying Files and Directories;The shutil Module;Command-Line Arguments with sys.argv;Argument Parsing with argparse;Running External Commands with subprocess;Handling Subprocess Results;Working Directory Management;Exit Status Codes;Platform Detection;Cross-Platform Paths;Permissions and Access Errors;Safe Shell and Subprocess Practices;Common OS Interaction Mistakes"),
    ("Virtual Environments and Package Management", "Introduction to Python Environments;Why Virtual Environments Matter;Creating Environments with venv;Activating an Environment on Windows;Activating an Environment on Linux and macOS;Deactivating an Environment;Installing Packages with pip;Upgrading Packages;Uninstalling Packages;Listing Installed Packages;Inspecting Package Details;requirements.txt;Generating Requirements Files;Installing from Requirements Files;Version Pinning;Dependency Conflicts;Understanding Wheels and Source Distributions;Installing Local Packages;Editable Installs;Introduction to pyproject.toml;Package Metadata;Publishing Packages Overview;Environment Variables and Secrets;Reproducible Python Environments;Common Package Management Mistakes"),
    ("Database Programming", "Introduction to Database Programming;Relational Databases Overview;SQLite with Python;Connecting to SQLite;Creating Database Tables;Inserting Records;Reading Records;Updating Records;Deleting Records;Parameterized SQL Queries;Database Transactions;Commit and Rollback;Closing Connections Safely;Handling Database Exceptions;Database Schema Design Basics;Primary Keys and Foreign Keys;Indexes and Query Performance;Connecting to PostgreSQL Overview;Connecting to MySQL Overview;Database Drivers and Dependencies;Object-Relational Mapping Overview;SQL Injection Prevention;Connection Management;Database Testing;Common Database Programming Mistakes"),
    ("Networking and APIs", "Introduction to Networking in Python;HTTP Basics;URLs and Query Parameters;The urllib Package;Sending HTTP Requests;Introduction to REST APIs;HTTP Methods;HTTP Status Codes;Request Headers;JSON API Responses;Query Parameters and Request Bodies;API Authentication Basics;API Keys and Environment Variables;Timeouts and Connection Errors;Handling HTTP Errors;Retry Strategies;Pagination;Rate Limits;Introduction to Third-Party HTTP Libraries;Using requests as an Optional Dependency;Using httpx as an Optional Dependency;Consuming Public APIs;Creating an API Client;Introduction to Sockets;TCP and UDP Concepts;Basic Socket Communication;Network Security Basics;Common Networking Mistakes"),
    ("Concurrency and Parallelism", "Introduction to Concurrency;Concurrency vs. Parallelism;Synchronous vs. Asynchronous Execution;Processes and Threads;The threading Module;Creating Threads;Joining Threads;Thread Synchronization;Locks and Race Conditions;Thread-Safe Programming;The queue Module;The multiprocessing Module;Creating Processes;Process Pools;The concurrent.futures Module;Thread Pools;Process Pools with Executors;Futures and Results;Exception Handling in Concurrent Tasks;The Global Interpreter Lock;CPU-Bound vs. I/O-Bound Tasks;Introduction to asyncio;Coroutines and async;await;Tasks and Event Loops;Asynchronous I/O;Choosing the Right Concurrency Model;Common Concurrency Mistakes"),
    ("Testing, Logging, and Debugging", "Introduction to Software Testing;Manual Testing;Unit Testing;The unittest Module;Test Cases and Test Suites;Assertions in Tests;Test Fixtures;Setup and Teardown;Testing Exceptions;Mocking Dependencies;Introduction to pytest;Test Discovery;Parameterized Tests;Test Coverage Concepts;Debugging with print();Debugging with pdb;IDE Debugging;Reading Tracebacks;The logging Module;Logging Levels;Logging to Files;Logging Formatting;Exception Logging;Assertions and Their Limitations;Reproducing Bugs;Regression Testing;Testing Best Practices;Common Testing and Debugging Mistakes"),
    ("Algorithms and Data Structures", "Introduction to Algorithms;Time Complexity;Space Complexity;Big O Notation;Best, Average, and Worst Cases;Arrays and Dynamic Arrays;Linked Lists;Stacks;Queues;Deques;Hash Tables;Dictionaries and Sets as Data Structures;Trees;Binary Trees;Binary Search Trees;Heaps and Priority Queues;Graphs;Graph Representations;Breadth-First Search;Depth-First Search;Recursion and Backtracking;Memoization;Dynamic Programming Basics;Greedy Algorithms;Divide and Conquer;Common Algorithmic Patterns;Practical Data Structure Selection"),
    ("Searching and Sorting Algorithms", "Introduction to Searching;Linear Search;Binary Search;Binary Search Prerequisites;Iterative Binary Search;Recursive Binary Search;Introduction to Sorting;Bubble Sort;Selection Sort;Insertion Sort;Merge Sort;Quick Sort;Heap Sort Overview;Counting Sort Overview;Python's Built-in sorted() Function;The List sort() Method;Sorting with key;Sorting with reverse;Stable Sorting;Custom Sorting;Sorting Dictionaries and Objects;Searching with bisect;Time and Space Complexity;Comparing Searching Algorithms;Comparing Sorting Algorithms;Common Searching and Sorting Mistakes"),
    ("Practice Programs", "Hello World;Display Personal Information;Add Two Numbers;Swap Two Variables;Calculate Rectangle Area;Celsius to Fahrenheit Converter;Simple Calculator;Even or Odd Checker;Positive, Negative, or Zero;Find the Largest of Three Numbers;Leap Year Checker;Multiplication Table;Sum of Natural Numbers;Factorial Calculator;Fibonacci Series;Prime Number Checker;Prime Numbers in a Range;Armstrong Number Checker;Palindrome Number Checker;Reverse a Number;Sum of Digits;Count Digits;Greatest Common Divisor;Least Common Multiple;Power Calculator;Decimal-to-Binary Conversion;List Sum and Average;Find Minimum and Maximum;Remove Duplicates from a List;Count Element Frequencies;Linear Search;Binary Search;Bubble Sort;Matrix Addition;Matrix Multiplication;Matrix Transpose;Reverse a String;String Palindrome Checker;Count Vowels and Consonants;Count Words in a String;Character Frequency Counter;Word Frequency Counter;Anagram Checker;Student Marks and Grade Calculator;Dictionary-Based Contact Book;Read and Write Text Files;CSV Data Analyzer;JSON Data Processor;Date Difference Calculator;Password Strength Checker;Number Guessing Game;Quiz Application;Expense Calculator;Basic API Data Fetcher;SQLite Student Record Program"),
    ("Mini Projects", "Project 1: Command-Line Calculator;Project 2: Student Management System;Project 3: Library Management System;Project 4: Contact Management System;Project 5: Bank Account Simulator;Project 6: Inventory Management System;Project 7: Employee Payroll System;Project 8: Quiz Application;Project 9: Number Guessing Game;Project 10: Tic-Tac-Toe;Project 11: Expense Tracker;Project 12: To-Do List Application;Project 13: Password Generator;Project 14: File Organizer;Project 15: Bulk File Renamer;Project 16: Text File Analyzer;Project 17: Weather API Client;Project 18: Currency Converter Using an API;Project 19: Web Scraper with Responsible Access;Project 20: SQLite-Based Inventory System;Project 21: Personal Finance Tracker;Project 22: Flashcard Learning App;Project 23: URL Shortener Prototype;Project 24: REST API with Flask or FastAPI;Project 25: Desktop Utility Application;Project Planning and Requirements;Project Architecture;Choosing Data Structures;Database and File Storage;Input Validation;Error Handling;Testing and Debugging;Dependency Management;Documentation and README Writing;Packaging and Deployment;Suggested Extensions and Challenges"),
    ("Interview Questions", "Basic Python Interview Questions;Python History and Features;Python Interpreter and Execution;Variables and Data Types;Mutable vs. Immutable Objects;Identity vs. Equality;Operators and Precedence;Conditions and Loops;Functions and Arguments;*args and **kwargs;Scope and Name Resolution;Lists, Tuples, Sets, and Dictionaries;List Comprehensions;Shallow Copy vs. Deep Copy;Iterators and Generators;Decorators and Closures;Object-Oriented Programming;Inheritance and Method Resolution Order;Special Methods;Exception Handling;Modules and Packages;File Handling;Context Managers;Regular Expressions;Memory Management;Garbage Collection;Python's Data Model;The Global Interpreter Lock;Threads vs. Processes;Asynchronous Programming;Testing and Mocking;Database Programming;REST APIs;Time and Space Complexity;Output Prediction Questions;Find-the-Bug Questions;Coding Interview Problems;Advanced Python Interview Questions"),
    ("Best Practices", "Writing Readable Python Code;Following PEP 8;Meaningful Naming Conventions;Consistent Formatting;Writing Useful Docstrings;Type Hints;Choosing Appropriate Data Structures;Writing Small, Focused Functions;Avoiding Unnecessary Global State;Using Comprehensions Carefully;Avoiding Mutable Default Arguments;Using Context Managers;Handling Exceptions Correctly;Avoiding Bare except Clauses;Logging Instead of Excessive Debug Prints;Managing Dependencies;Using Virtual Environments;Protecting Secrets and Credentials;Validating External Input;Safe File Handling;Safe SQL Query Practices;Writing Unit Tests;Testable Code Design;Profiling Before Optimization;Avoiding Premature Optimization;Documentation and README Practices;Code Review Checklist;Python Project Structure;Security and Dependency Updates"),
    ("Common Errors and Debugging", "Syntax Errors;Indentation Errors;Name Errors;Type Errors;Value Errors;Index Errors;Key Errors;Attribute Errors;Import Errors;Module Not Found Errors;Zero Division Errors;File Not Found Errors;Permission Errors;Unbound Local Errors;Recursion Errors;Runtime Errors;Logic Errors;Mutable Default Argument Bugs;Shallow Copy and Aliasing Bugs;Incorrect String Comparisons;Floating-Point Precision Issues;Incorrect Exception Handling;File Resource Leaks;Circular Import Problems;Dependency Conflicts;Virtual Environment Problems;Infinite Loops;Off-by-One Errors;Debugging with Tracebacks;Debugging with pdb;Debugging in VS Code;Using Assertions Effectively;Logging for Troubleshooting;Reproducing and Isolating Bugs;Debugging Checklist"),
    ("Python Keywords and Operator Precedence", "Complete Python Keyword Reference;Reserved Keywords;Soft Keywords;The False, True, and None Constants;and, or, and not;if, elif, and else;for, while, break, and continue;try, except, finally, and raise;def, return, yield, and lambda;class, self Convention, and super();import, from, and as;global and nonlocal;with and async with;async and await;match and case;pass, del, and assert;is and in;Arithmetic Operator Precedence;Exponentiation Precedence;Unary Operator Precedence;Shift and Bitwise Precedence;Comparison Operator Precedence;Logical Operator Precedence;Conditional Expressions;Assignment Expressions;Assignment Operator Behavior;Parentheses and Expression Grouping;Chained Comparisons;Short-Circuit Evaluation;Evaluation Order;Common Precedence Traps;Version-Specific Language Features"),
    ("Complete Python Quick Reference", "Basic Python Program Template;Running Python Scripts;Interactive Python Commands;Virtual Environment Commands;pip Package Management Commands;Variables and Assignment Syntax;Built-in Data Types;Type Checking Functions;Type Conversion Functions;Input and Output Syntax;String Formatting Reference;Operator Quick Reference;Conditional Statement Syntax;Loop Syntax;Function Definition Syntax;Argument Types;Lambda Function Syntax;List Method Reference;Tuple Operations;Dictionary Method Reference;Set Operation Reference;String Method Reference;Comprehension Syntax;Exception Handling Syntax;Class and Object Syntax;Inheritance Syntax;Special Method Reference;Module and Package Syntax;File Handling Syntax;Path Handling Reference;JSON and CSV Reference;Date and Time Reference;Regular Expression Reference;Common Standard Library Modules;Functional Programming Reference;Iterator and Generator Reference;Decorator Reference;Database Programming Reference;Networking and API Reference;Concurrency Reference;Testing and Debugging Reference;Searching Algorithm Reference;Sorting Algorithm Reference;Common Exception Reference;Common Built-in Functions;Common Built-in Types and Methods;Type Hinting Reference;Python Environment Checklist;Code Quality Checklist;Security Checklist;Python Version Compatibility Notes;Essential Python Programming Patterns;Final Python Programming Checklist"),
]


def make_c_topic_items(title):
    """Build structured, C11-oriented content items for a syllabus topic."""
    focus = title.split(" — ", 1)[0]
    lower = focus.lower()
    category_examples = [
        (("variable", "constant", "data type", "literal", "sizeof"), "#include <stdio.h>\n\nint main(void) {\n    const int count = 3;\n    printf(\"count=%d, bytes=%zu\\n\", count, sizeof count);\n    return 0;\n}", "count=3, bytes=4"),
        (("input", "output", "printf", "scanf", "getchar", "putchar", "fgets", "puts", "format", "buffer", "escape"), "#include <stdio.h>\n\nint main(void) {\n    char name[32] = \"Ada\";\n    printf(\"Hello, %s!\\n\", name);\n    return 0;\n}", "Hello, Ada!"),
        (("decision", "condition", "if", "switch", "ternary", "operator", "conversion", "cast"), "#include <stdio.h>\n\nint main(void) {\n    int value = 7;\n    if (value % 2 == 0) puts(\"even\");\n    else puts(\"odd\");\n    return 0;\n}", "odd"),
        (("loop", "iteration", "break", "continue", "goto", "counter", "sentinel", "tracing"), "#include <stdio.h>\n\nint main(void) {\n    for (int i = 1; i <= 3; ++i) printf(\"%d \", i);\n    putchar('\\n');\n    return 0;\n}", "1 2 3"),
        (("array", "search", "sort", "binary", "linear", "matrix", "multidimensional"), "#include <stdio.h>\n\nint main(void) {\n    int values[] = {4, 7, 2};\n    size_t length = sizeof values / sizeof values[0];\n    for (size_t i = 0; i < length; ++i) printf(\"%d \", values[i]);\n    putchar('\\n');\n    return 0;\n}", "4 7 2"),
        (("string", "character", "ctype", "tolower", "toupper", "null terminator"), "#include <stdio.h>\n#include <string.h>\n\nint main(void) {\n    char word[] = \"C11\";\n    printf(\"%zu: %s\\n\", strlen(word), word);\n    return 0;\n}", "3: C11"),
        (("pointer", "address", "dereference", "dangling", "wild", "void pointer", "function pointer"), "#include <stdio.h>\n\nint main(void) {\n    int value = 42;\n    int *pointer = &value;\n    printf(\"%d\\n\", *pointer);\n    return 0;\n}", "42"),
        (("function", "recursion", "parameter", "argument", "return value", "prototype"), "#include <stdio.h>\n\nstatic int square(int value) { return value * value; }\n\nint main(void) {\n    printf(\"%d\\n\", square(5));\n    return 0;\n}", "25"),
        (("structure", "struct", "union", "enum", "enumeration", "typedef"), "#include <stdio.h>\n\nstruct Point { int x; int y; };\n\nint main(void) {\n    struct Point point = {.x = 2, .y = 5};\n    printf(\"(%d, %d)\\n\", point.x, point.y);\n    return 0;\n}", "(2, 5)"),
        (("dynamic memory", "malloc", "calloc", "realloc", "free", "heap", "memory leak"), "#include <stdio.h>\n#include <stdlib.h>\n\nint main(void) {\n    int *value = malloc(sizeof *value);\n    if (value == NULL) return 1;\n    *value = 9;\n    printf(\"%d\\n\", *value);\n    free(value);\n    return 0;\n}", "9"),
        (("file", "fopen", "fclose", "fread", "fwrite", "fseek", "ftell"), "#include <stdio.h>\n\nint main(void) {\n    FILE *file = tmpfile();\n    if (file == NULL) return 1;\n    fputs(\"C file I/O\\n\", file);\n    rewind(file);\n    char line[32];\n    if (fgets(line, sizeof line, file) != NULL) fputs(line, stdout);\n    fclose(file);\n    return 0;\n}", "C file I/O"),
    ]


def make_python_topic_items(title):
    """Build structured, runnable Python 3 learning items for one topic."""
    keywords = title.lower()
    examples = [
        (("list", "array", "stack", "queue", "sort", "search", "matrix"), "values = [4, 7, 2]\nprint(sorted(values))", "[2, 4, 7]"),
        (("dictionary", "dict", "frequency", "hash", "json"), "person = {\"name\": \"Ada\", \"level\": 3}\nprint(person[\"name\"])\nprint(person[\"level\"])", "Ada\n3"),
        (("set", "unique", "union", "intersection"), "left = {1, 2, 3}\nright = {3, 4}\nprint(sorted(left & right))", "[3]"),
        (("tuple", "immutable", "unpacking", "named tuple"), "coordinates = (4, 9)\nx, y = coordinates\nprint(x, y)", "4 9"),
        (("string", "text", "character", "regex", "regular expression", "encoding"), "message = \"Python 3\"\nprint(message.upper())\nprint(len(message))", "PYTHON 3\n8"),
        (("file", "path", "directory", "csv", "xml", "toml", "format", "serialize"), "from pathlib import Path\n\npath = Path(\"example.txt\")\nprint(path.suffix or \"no extension\")", "txt"),
        (("function", "argument", "parameter", "lambda", "decorator", "closure", "recursion"), "def square(number: int) -> int:\n    return number * number\n\nprint(square(5))", "25"),
        (("class", "object", "oop", "inheritance", "method", "dataclass", "polymorphism"), "class Greeter:\n    def greet(self, name: str) -> str:\n        return f\"Hello, {name}!\"\n\nprint(Greeter().greet(\"Ada\"))", "Hello, Ada!"),
        (("exception", "error", "assert", "debug", "traceback"), "text = \"42\"\ntry:\n    number = int(text)\nexcept ValueError:\n    print(\"Invalid number\")\nelse:\n    print(number)", "42"),
        (("loop", "iteration", "iterator", "generator", "comprehension", "yield", "enumerate", "zip"), "squares = [number * number for number in range(1, 4)]\nprint(squares)", "[1, 4, 9]"),
        (("date", "time", "calendar", "timestamp", "datetime", "zone"), "from datetime import date\n\ntoday = date(2025, 1, 1)\nprint(today.isoformat())", "2025-01-01"),
        (("database", "sqlite", "sql", "transaction"), "import sqlite3\n\nwith sqlite3.connect(\":memory:\") as connection:\n    connection.execute(\"CREATE TABLE item (name TEXT)\")\n    connection.execute(\"INSERT INTO item VALUES (?)\", (\"book\",))\n    row = connection.execute(\"SELECT name FROM item\").fetchone()\n    print(row[0])", "book"),
        (("operator", "condition", "decision", "boolean", "truth", "precedence", "conversion", "type"), "score = 82\nresult = \"pass\" if score >= 60 else \"retry\"\nprint(result)", "pass"),
    ]
    code, expected = next(
        ((snippet, output) for terms, snippet, output in examples if any(term in keywords for term in terms)),
        ("def main() -> None:\n    print(\"Python 3 example\")\n\nif __name__ == \"__main__\":\n    main()", "Python 3 example"),
    )
    feature_note = "Use Python 3 syntax; verify the minimum supported version for newer features such as match/case, tomllib, and functools.cache."
    if "python 3.10" in keywords or "match-case" in keywords or "match and case" in keywords:
        code = "value = 2\nmatch value:\n    case 1:\n        result = \"one\"\n    case 2:\n        result = \"two\"\n    case _:\n        result = \"other\"\nprint(result)"
        expected = "two"
        feature_note = "Requires Python 3.10 or newer: structural pattern matching uses match/case."
    return [
        heading_item(title),
        para_item(f"{title} is a practical Python concept. Learn its purpose, the rules that affect its behavior, and how it fits into a readable, maintainable program."),
        note_item(f"Syntax and version note: {title}. {feature_note}"),
        {"type": "code", "data": {"title": title + " — Python 3 example", "code": code, "language": "python"}},
        {"type": "output", "data": {"text": expected}},
        tip_item("Prefer clear names, small examples, and standard-library tools. Run examples with the same Python version used by your project."),
        warning_item("Validate external input, handle expected exceptions, and avoid unsafe evaluation or exposing credentials in source code."),
    ]
    code, expected = next(
        (example, output)
        for keywords, example, output in category_examples
        if any(keyword in lower for keyword in keywords)
    ) if any(any(keyword in lower for keyword in keywords) for keywords, _, _ in category_examples) else (
        "#include <stdio.h>\n\nint main(void) {\n    puts(\"C11 reference example\");\n    return 0;\n}",
        "C11 reference example",
    )
    explanation = (
        f"{focus} explains a C concept used to design and maintain programs. "
        "Learn the rule, where it applies, and what assumptions the C standard permits. "
        "Use the example as a starting point and adapt names and values to your problem."
    )
    return [
        heading_item(title),
        para_item(explanation),
        note_item(f"C11 syntax and usage: {focus}. Check the relevant declaration, operand types, bounds, and library return values."),
        code_item(title + " — C11 example", code, "c"),
        {"type": "output", "data": {"text": expected}},
        tip_item("Compile with a C11 compiler and enable warnings, for example: cc -std=c11 -Wall -Wextra -pedantic program.c -o program."),
        warning_item("Do not assume behavior that the C standard leaves undefined or implementation-defined; validate bounds, inputs, and function results."),
    ]


class Command(BaseCommand):
    help = "Seed database with Django, React, Java, Python, C cheat sheet content"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding languages...\n")
        total_subsections = 0

        c_language = Language.objects.filter(slug="c").first()
        if c_language:
            with transaction.atomic():
                c_language.sections.all().delete()
                for part_order, (part_title, topic_list) in enumerate(C_CHEAT_SHEET, start=1):
                    section = Section.objects.create(
                        language=c_language,
                        title=f"Part {part_order:02d} - {part_title}",
                        slug=slugify(f"part-{part_order:02d}-{part_title}"),
                        description=f"C11 learning topics covering {part_title.lower()}.",
                        display_order=part_order - 1,
                        status="active",
                    )
                    topics = topic_list.split(";")
                    subsections = [
                        Subsection(
                            section=section,
                            title=topic_title,
                            slug=slugify(topic_title)[:200].strip("-") or f"topic-{topic_order}",
                            description=f"C11 reference and learning notes for {topic_title}.",
                            display_order=topic_order - 1,
                            status="active",
                        )
                        for topic_order, topic_title in enumerate(topics, start=1)
                    ]
                    Subsection.objects.bulk_create(subsections)
                    all_items = []
                    for subsection, topic_title in zip(subsections, topics):
                        all_items.extend(
                            ContentItem(
                                subsection=subsection,
                                type=item_data["type"],
                                data=item_data["data"],
                                display_order=item_order,
                                status="active",
                            )
                            for item_order, item_data in enumerate(make_c_topic_items(topic_title))
                        )
                    ContentItem.objects.bulk_create(all_items)
                    total_subsections += len(topics)
                self.stdout.write(f"  Replaced C course with {len(C_CHEAT_SHEET)} parts.")

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

            if lang_data["slug"] == "c":
                continue

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
            f"\nDone! 5 languages, {total_subsections} subsections with code/content items created."
        ))
