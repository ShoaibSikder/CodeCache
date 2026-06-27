"""
Management command to seed JavaScript cheat sheet content into the database.
Usage: python manage.py seed_javascript
"""
from django.core.management.base import BaseCommand
from apps.languages.models import Language
from apps.content.models import Section, Subsection, ContentItem


class Command(BaseCommand):
    help = 'Seeds the database with JavaScript cheat sheet content'

    def handle(self, *args, **options):
        # Create or get the JavaScript language
        lang, created = Language.objects.get_or_create(
            slug='javascript',
            defaults={
                'name': 'JavaScript',
                'description': 'A comprehensive JavaScript cheat sheet and reference guide covering all core concepts from basics to ES6 features.',
                'status': 'active',
                'display_order': 1,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created language: {lang.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Language already exists: {lang.name}'))
            # Clear existing content to re-seed
            Section.objects.filter(language=lang).delete()

        # ============================================================
        # SECTION 1: JavaScript Basics
        # ============================================================
        s1 = Section.objects.create(
            language=lang, title='1. JavaScript Basics', slug='javascript-basics',
            description='Getting started with JavaScript — internal and external scripts.',
            display_order=1, status='active'
        )
        sub = Subsection.objects.create(section=s1, title='Internal JavaScript', slug='internal-javascript', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='paragraph', data={'text': 'Embed JavaScript directly inside an HTML file using the <script> tag.'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '<script>\n    console.log("Hello JavaScript");\n</script>', 'language': 'html'}, display_order=2, status='active')

        sub = Subsection.objects.create(section=s1, title='External JavaScript', slug='external-javascript', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='paragraph', data={'text': 'Link an external .js file for better organization.'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '<script src="app.js"></script>', 'language': 'html'}, display_order=2, status='active')

        # ============================================================
        # SECTION 2: Comments
        # ============================================================
        s2 = Section.objects.create(
            language=lang, title='2. Comments', slug='comments',
            description='Single-line and multi-line comments in JavaScript.',
            display_order=2, status='active'
        )
        sub = Subsection.objects.create(section=s2, title='Single-Line Comment', slug='single-line-comment', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '// This is a comment', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s2, title='Multi-Line Comment', slug='multi-line-comment', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '/*\n   Multi-line\n   comment\n*/', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 3: Variables
        # ============================================================
        s3 = Section.objects.create(
            language=lang, title='3. Variables', slug='variables',
            description='Variable declarations using var, let, and const.',
            display_order=3, status='active'
        )
        sub = Subsection.objects.create(section=s3, title='var', slug='var', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'var name = "Shoaib";', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s3, title='let', slug='let', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let age = 24;', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s3, title='const', slug='const', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const PI = 3.14159;', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s3, title='Recommended Usage', slug='recommended-usage', display_order=4, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'Use const by default. Use let when values change. Avoid var in modern JavaScript due to function-scoping issues.'}, display_order=1, status='active')

        # ============================================================
        # SECTION 4: Data Types
        # ============================================================
        s4 = Section.objects.create(
            language=lang, title='4. Data Types', slug='data-types',
            description='Primitive and non-primitive data types in JavaScript.',
            display_order=4, status='active'
        )
        sub = Subsection.objects.create(section=s4, title='Primitive Types', slug='primitive-types', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let name = "Shoaib";      // String\nlet age = 24;             // Number\nlet isStudent = true;     // Boolean\nlet value = null;         // Null\nlet city;                 // Undefined\nlet id = Symbol("user");  // Symbol', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s4, title='Non-Primitive Types', slug='non-primitive-types', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='heading', data={'text': 'Object'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const student = {\n    name: "Shoaib",\n    age: 24\n};', 'language': 'javascript'}, display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='heading', data={'text': 'Array'}, display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const numbers = [10, 20, 30];', 'language': 'javascript'}, display_order=4, status='active')
        ContentItem.objects.create(subsection=sub, type='heading', data={'text': 'Function'}, display_order=5, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'function greet() {\n    console.log("Hello");\n}', 'language': 'javascript'}, display_order=6, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'JavaScript distinguishes between primitive values and reference types such as objects, arrays, and functions.'}, display_order=7, status='active')

        # ============================================================
        # SECTION 5: Output
        # ============================================================
        s5 = Section.objects.create(
            language=lang, title='5. Output', slug='output',
            description='Ways to display output in JavaScript.',
            display_order=5, status='active'
        )
        sub = Subsection.objects.create(section=s5, title='Console Output', slug='console-output', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'console.log("Hello");\nconsole.warn("Warning");\nconsole.error("Error");', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s5, title='Alert Box', slug='alert-box', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'alert("Welcome");', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 6: User Input
        # ============================================================
        s6 = Section.objects.create(
            language=lang, title='6. User Input', slug='user-input',
            description='Getting user input via prompt and confirm.',
            display_order=6, status='active'
        )
        sub = Subsection.objects.create(section=s6, title='Prompt', slug='prompt', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let name = prompt("Enter your name");', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s6, title='Confirm', slug='confirm', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let result = confirm("Continue?");', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 7: Operators
        # ============================================================
        s7 = Section.objects.create(
            language=lang, title='7. Operators', slug='operators',
            description='All JavaScript operators — arithmetic, assignment, comparison, logical, and bitwise.',
            display_order=7, status='active'
        )
        sub = Subsection.objects.create(section=s7, title='Arithmetic Operators', slug='arithmetic-operators', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '+  -  *  /  %  **  ++  --', 'language': 'text'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let a = 10;\nlet b = 3;\nconsole.log(a + b);   // 13\nconsole.log(a ** b);  // 1000', 'language': 'javascript'}, display_order=2, status='active')

        sub = Subsection.objects.create(section=s7, title='Assignment Operators', slug='assignment-operators', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '=  +=  -=  *=  /=  %=', 'language': 'text'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s7, title='Comparison Operators', slug='comparison-operators', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '==  ===  !=  !==  >  <  >=  <=', 'language': 'text'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'console.log(5 === "5"); // false', 'language': 'javascript'}, display_order=2, status='active')

        sub = Subsection.objects.create(section=s7, title='Logical Operators', slug='logical-operators', display_order=4, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '&&  ||  !', 'language': 'text'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let age = 20;\nconsole.log(age >= 18 && age <= 60); // true', 'language': 'javascript'}, display_order=2, status='active')

        sub = Subsection.objects.create(section=s7, title='Bitwise Operators', slug='bitwise-operators', display_order=5, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '&  |  ^  ~  <<  >>', 'language': 'text'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'JavaScript supports arithmetic, comparison, logical, assignment, and bitwise operators for working with values and expressions.'}, display_order=2, status='active')

        # ============================================================
        # SECTION 8: Type Conversion
        # ============================================================
        s8 = Section.objects.create(
            language=lang, title='8. Type Conversion', slug='type-conversion',
            description='Converting between data types in JavaScript.',
            display_order=8, status='active'
        )
        sub = Subsection.objects.create(section=s8, title='String to Number', slug='string-to-number', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let num = Number("100");\nlet num = parseInt("100");\nlet num = parseFloat("10.5");', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s8, title='Number to String', slug='number-to-string', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let text = String(100);', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s8, title='Check NaN', slug='check-nan', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'isNaN("Hello");  // true', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 9: Scope
        # ============================================================
        s9 = Section.objects.create(
            language=lang, title='9. Scope', slug='scope',
            description='Understanding global, function, and block scope.',
            display_order=9, status='active'
        )
        sub = Subsection.objects.create(section=s9, title='Global Scope', slug='global-scope', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let a = 10;', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s9, title='Function Scope', slug='function-scope', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'function test() {\n    let b = 20;\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s9, title='Block Scope', slug='block-scope', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'if (true) {\n    let x = 50;\n}', 'language': 'javascript'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'Variables declared with let and const are block scoped, while var follows function scope rules.'}, display_order=2, status='active')

        # ============================================================
        # SECTION 10: Conditional Statements
        # ============================================================
        s10 = Section.objects.create(
            language=lang, title='10. Conditional Statements', slug='conditional-statements',
            description='if, else-if, ternary operator, and switch statements.',
            display_order=10, status='active'
        )
        sub = Subsection.objects.create(section=s10, title='if', slug='if', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'if (age >= 18) {\n    console.log("Adult");\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s10, title='if-else', slug='if-else', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'if (age >= 18) {\n    console.log("Adult");\n} else {\n    console.log("Minor");\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s10, title='else-if', slug='else-if', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'if (marks >= 80) {\n    console.log("A+");\n} else if (marks >= 70) {\n    console.log("A");\n} else {\n    console.log("B");\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s10, title='Ternary Operator', slug='ternary-operator', display_order=4, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let result = (age >= 18) ? "Adult" : "Minor";', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s10, title='Switch', slug='switch', display_order=5, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'switch (day) {\n    case 1:\n        console.log("Monday");\n        break;\n    case 2:\n        console.log("Tuesday");\n        break;\n    default:\n        console.log("Invalid");\n}', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 11: Loops
        # ============================================================
        s11 = Section.objects.create(
            language=lang, title='11. Loops', slug='loops',
            description='All looping constructs — for, while, do-while, for...of, for...in.',
            display_order=11, status='active'
        )
        sub = Subsection.objects.create(section=s11, title='for Loop', slug='for-loop', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'for (let i = 0; i < 5; i++) {\n    console.log(i);\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s11, title='while Loop', slug='while-loop', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let i = 0;\nwhile (i < 5) {\n    console.log(i);\n    i++;\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s11, title='do-while Loop', slug='do-while-loop', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let i = 0;\ndo {\n    console.log(i);\n    i++;\n} while (i < 5);', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s11, title='for...of', slug='for-of', display_order=4, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const nums = [10, 20, 30];\nfor (let num of nums) {\n    console.log(num);\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s11, title='for...in', slug='for-in', display_order=5, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const student = { name: "Shoaib", age: 24 };\nfor (let key in student) {\n    console.log(key);\n}', 'language': 'javascript'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'JavaScript provides multiple looping mechanisms for arrays, objects, and repeated execution.'}, display_order=2, status='active')

        # ============================================================
        # SECTION 12: Functions
        # ============================================================
        s12 = Section.objects.create(
            language=lang, title='12. Functions', slug='functions',
            description='Function declarations, arrow functions, and anonymous functions.',
            display_order=12, status='active'
        )
        sub = Subsection.objects.create(section=s12, title='Function Declaration', slug='function-declaration', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'function greet() {\n    console.log("Hello");\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s12, title='Function with Parameters', slug='function-with-parameters', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'function add(a, b) {\n    return a + b;\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s12, title='Function Call', slug='function-call', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'add(5, 3);  // returns 8', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s12, title='Arrow Function', slug='arrow-function', display_order=4, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const add = (a, b) => a + b;', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s12, title='Anonymous Function', slug='anonymous-function', display_order=5, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const greet = function() {\n    console.log("Hello");\n};', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 13: Arrays
        # ============================================================
        s13 = Section.objects.create(
            language=lang, title='13. Arrays', slug='arrays',
            description='Creating, accessing, and manipulating arrays with built-in methods.',
            display_order=13, status='active'
        )
        sub = Subsection.objects.create(section=s13, title='Create Array', slug='create-array', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const numbers = [10, 20, 30];', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s13, title='Access Elements', slug='access-elements', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'numbers[0];  // 10', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s13, title='Common Array Methods', slug='common-array-methods', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': '// push() - add to end\nnumbers.push(40);\n\n// pop() - remove from end\nnumbers.pop();\n\n// shift() - remove from start\nnumbers.shift();\n\n// unshift() - add to start\nnumbers.unshift(5);\n\n// concat() - merge arrays\nlet arr3 = arr1.concat(arr2);\n\n// slice() - extract portion\nnumbers.slice(1, 3);\n\n// splice() - remove/replace items\nnumbers.splice(1, 2);', 'language': 'javascript'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'JavaScript arrays provide methods for insertion, deletion, searching, and merging collections.'}, display_order=2, status='active')

        # ============================================================
        # SECTION 14: Strings
        # ============================================================
        s14 = Section.objects.create(
            language=lang, title='14. Strings', slug='strings',
            description='String declaration and common string manipulation methods.',
            display_order=14, status='active'
        )
        sub = Subsection.objects.create(section=s14, title='String Methods', slug='string-methods', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let name = "JavaScript";\n\nname.length;              // 10\nname.toUpperCase();       // "JAVASCRIPT"\nname.toLowerCase();       // "javascript"\nname.replace("Java","Type"); // "TypeScript"\nname.slice(0, 4);        // "Java"\nname.substring(0, 4);    // "Java"\n\n// Concatenation\nlet full = first.concat(last);', 'language': 'javascript'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'String manipulation is one of the most common JavaScript tasks and is supported through many built-in methods.'}, display_order=2, status='active')

        # ============================================================
        # SECTION 15: Objects
        # ============================================================
        s15 = Section.objects.create(
            language=lang, title='15. Objects', slug='objects',
            description='Creating, accessing, and modifying JavaScript objects.',
            display_order=15, status='active'
        )
        sub = Subsection.objects.create(section=s15, title='Create Object', slug='create-object', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const student = {\n    name: "Shoaib",\n    age: 24,\n    greet() {\n        console.log("Hello");\n    }\n};', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s15, title='Access Property', slug='access-property', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'student.name;      // "Shoaib"\nstudent["age"];     // 24', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s15, title='Add Property', slug='add-property', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'student.cgpa = 3.8;', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s15, title='Delete Property', slug='delete-property', display_order=4, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'delete student.age;', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 16: Regular Expressions
        # ============================================================
        s16 = Section.objects.create(
            language=lang, title='16. Regular Expressions', slug='regular-expressions',
            description='Creating and using regular expressions for pattern matching.',
            display_order=16, status='active'
        )
        sub = Subsection.objects.create(section=s16, title='Regex Basics', slug='regex-basics', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const pattern = /hello/;\npattern.test("hello world");  // true\n\n// Common patterns\n/\\d/     // Match digits\n/\\s/     // Match whitespace\n/[abc]/  // Match characters a, b, or c', 'language': 'javascript'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'Regular expressions help perform searching, validation, and text replacement operations.'}, display_order=2, status='active')

        # ============================================================
        # SECTION 17: Events
        # ============================================================
        s17 = Section.objects.create(
            language=lang, title='17. Events', slug='events',
            description='Handling browser events like clicks, keyboard input, and form submissions.',
            display_order=17, status='active'
        )
        sub = Subsection.objects.create(section=s17, title='Click Event', slug='click-event', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'button.onclick = function() {\n    alert("Clicked");\n};', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s17, title='addEventListener()', slug='addeventlistener', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'button.addEventListener("click", function() {\n    console.log("Clicked");\n});', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s17, title='Common Events', slug='common-events', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='table', data={
            'columns': ['Event', 'Description'],
            'rows': [
                ['click', 'Mouse click'],
                ['dblclick', 'Double click'],
                ['keyup', 'Key released'],
                ['keydown', 'Key pressed'],
                ['mouseover', 'Mouse enters'],
                ['mouseout', 'Mouse leaves'],
                ['change', 'Value changed'],
                ['submit', 'Form submitted'],
                ['focus', 'Input focused'],
                ['blur', 'Input loses focus'],
                ['load', 'Page loaded'],
            ]
        }, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'JavaScript events make web pages interactive and responsive to user actions.'}, display_order=2, status='active')

        # ============================================================
        # SECTION 18: DOM Manipulation
        # ============================================================
        s18 = Section.objects.create(
            language=lang, title='18. DOM Manipulation', slug='dom-manipulation',
            description='Selecting and modifying HTML elements using the DOM API.',
            display_order=18, status='active'
        )
        sub = Subsection.objects.create(section=s18, title='Select Element', slug='select-element', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'document.getElementById("title");\ndocument.querySelector(".box");\ndocument.querySelectorAll("p");', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s18, title='Change Content', slug='change-content', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'element.innerHTML = "New Content";\nelement.textContent = "Hello";', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s18, title='Change Style', slug='change-style', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'element.style.color = "red";', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 19: Exception Handling
        # ============================================================
        s19 = Section.objects.create(
            language=lang, title='19. Exception Handling', slug='exception-handling',
            description='Try-catch-finally and throwing errors.',
            display_order=19, status='active'
        )
        sub = Subsection.objects.create(section=s19, title='Try Catch', slug='try-catch', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'try {\n    let x = y;\n} catch (error) {\n    console.log(error);\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s19, title='Finally', slug='finally', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'finally {\n    console.log("Done");\n}', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s19, title='Throw', slug='throw', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'throw "Invalid Input";', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 20: Window Object
        # ============================================================
        s20 = Section.objects.create(
            language=lang, title='20. Window Object', slug='window-object',
            description='Browser window object methods and properties.',
            display_order=20, status='active'
        )
        sub = Subsection.objects.create(section=s20, title='Window Methods', slug='window-methods', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'window.alert("Hello");\nwindow.location.href;\nwindow.location.reload();\nwindow.open("https://example.com");', 'language': 'javascript'}, display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='note', data={'text': 'The window object represents the browser window and provides access to browser-related functionality.'}, display_order=2, status='active')

        # ============================================================
        # SECTION 21: JSON
        # ============================================================
        s21 = Section.objects.create(
            language=lang, title='21. JSON', slug='json',
            description='Converting between JavaScript objects and JSON strings.',
            display_order=21, status='active'
        )
        sub = Subsection.objects.create(section=s21, title='Object to JSON', slug='object-to-json', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const json = JSON.stringify(student);', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s21, title='JSON to Object', slug='json-to-object', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const obj = JSON.parse(json);', 'language': 'javascript'}, display_order=1, status='active')

        # ============================================================
        # SECTION 22: ES6 Features
        # ============================================================
        s22 = Section.objects.create(
            language=lang, title='22. ES6 Features', slug='es6-features',
            description='Modern JavaScript features — template literals, destructuring, spread operator, and default parameters.',
            display_order=22, status='active'
        )
        sub = Subsection.objects.create(section=s22, title='Template Literals', slug='template-literals', display_order=1, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'let name = "Shoaib";\nconsole.log(`Hello ${name}`);', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s22, title='Destructuring', slug='destructuring', display_order=2, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const person = { name: "Shoaib", age: 24 };\nconst { name, age } = person;', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s22, title='Spread Operator', slug='spread-operator', display_order=3, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'const arr = [1, 2, 3];\nconst newArr = [...arr, 4, 5];', 'language': 'javascript'}, display_order=1, status='active')

        sub = Subsection.objects.create(section=s22, title='Default Parameters', slug='default-parameters', display_order=4, status='active')
        ContentItem.objects.create(subsection=sub, type='code', data={'code': 'function greet(name = "Guest") {\n    console.log(name);\n}', 'language': 'javascript'}, display_order=1, status='active')

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {lang.section_count} sections with JavaScript cheat sheet content!'
        ))