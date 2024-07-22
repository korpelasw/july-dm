from flask import Flask, render_template, jsonify, request, redirect, url_for, render_template_string, session
from flask_sqlalchemy import SQLAlchemy
import time, random, math, os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # You need to set a secret key for sessions

matrix_data = [[{'title': f'Row {i}, Col {j}'} for j in range(3)] for i in range(3)]

# Use the DATABASE_URL environment variable from Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define a dictionary to store the current button texts
button_texts = {}

# Initialize button states
button_states = {
    'clickButton1': False,
    'clickButton2': False,
    'clickButton3': False,
    'clickButton4': False,
    'clickButton5': False,
    'clickButton6': False,
    'clickButton7': False,
    'clickButtonA': False,
    'clickButtonB': False,
    'clickButtonC': False,
    'clickButtonD': False,
    'extraButton1': False,
    'extraButton2': False
}


task_states = {
    'task1': 'not completed',
    'task2': 'not completed',
    'task3': 'not completed',
    'task4': 'not completed',
    'task6': 'not completed',
    # Add more tasks as needed
}

task_buttons = {
    'task1': ['clickButton1', 'clickButton2', 'clickButton3', 'clickButton4','clickButton5','clickButton6', 'clickButton7'],
    'task2': ['clickButton5', 'clickButton6'],  # Add buttons for task2
    'task3': ['clickButton5', 'clickButton6'],
    'task4': ['clickButtonA', 'clickButtonB', 'clickButtonC', 'clickButtonD'],
    'task6': ['extraButton1', 'extraButton2'],
    # Add more tasks as needed
}

@app.route('/create_single_button')
def create_single_button(position, color, text):
    width = 150
    button_id = 'singleButton'  # Unique button ID
    
    button_html = f'<button id="{button_id}" style="width: {width}px; height: 40px; background-color: {color}; border-radius: 10px; position: fixed; top: {position}%; left: 30%; font-size: 16px; font-family: Verdana; transform: translate(-50%, -50%);">{text}</button>'
    
    return button_html



def get_task_state(task_name, random_number):
    global highest_price_details
    highest_price_button = highest_price_details.get('button_id')

    if task_name == 'task1':
        if button_states.get('clickButtonA') and highest_price_button == 'button-1-3':
            return 'completed'
        elif button_states.get('clickButtonB') and highest_price_button == 'button-2-3':
            return 'completed'
        elif button_states.get('clickButtonC') and highest_price_button == 'button-3-3':
            return 'completed'
        else:
            return 'not completed'

    elif task_name == 'task2':
        if button_states['clickButton5'] and negative_count2 < negative_count1:
            return 'completed'
        elif button_states['clickButton6'] and negative_count1 < negative_count2:
            return 'completed'
        else:
            return 'not completed'  
    elif task_name == 'task3':
        if button_states['clickButton5'] and negative_count2 < negative_count1:
            return 'completed'
        elif button_states['clickButton6'] and negative_count1 < negative_count2:
            return 'completed'
        else:
            return 'not completed'
    elif task_name == 'task4':
        if button_states.get('clickButtonA') and highest_price_button == 'button-1-3':
            return 'completed'
        elif button_states.get('clickButtonB') and highest_price_button == 'button-2-3':
            return 'completed'
        elif button_states.get('clickButtonC') and highest_price_button == 'button-3-3':
            return 'completed'
        else:
            return 'not completed'
    
def generate_random_positions(button_count, screen_width, screen_height, button_width, button_height):
    positions = []
    attempts = 0

    while len(positions) < button_count and attempts < 1000:
        new_position = (random.randint(0, screen_width - button_width),
                        random.randint(0, screen_height - button_height))
        
        # Check for overlaps
        if all(math.hypot(new_position[0] - pos[0], new_position[1] - pos[1]) > button_width for pos in positions):
            positions.append(new_position)
        
        attempts += 1

    if len(positions) < button_count:
        raise Exception("Could not generate non-overlapping positions for all buttons")

    return positions

# Example usage:
button_count = 10
screen_width = 800
screen_height = 600
button_width = 100
button_height = 50

button_positions = generate_random_positions(button_count, screen_width, screen_height, button_width, button_height)
print(button_positions)

    # Add more tasks as needed
highest_price_details = {}

def find_highest_price():
    global highest_price_details
    highest_price = 0
    highest_price_button = ''
    
    for button_id, text in button_texts.items():
        if button_id.endswith('-3'):  # Check only price buttons
            try:
                # Remove any non-numeric characters and convert to integer
                price = int(''.join(filter(str.isdigit, text)))
                if price > highest_price:
                    highest_price = price
                    highest_price_button = button_id
            except ValueError:
                # Handle the case where conversion to integer fails
                continue
    
    highest_price_details = {'button_id': highest_price_button, 'price': highest_price}
    return highest_price_button, highest_price


def reset_button_press_count():
    global try_again_button_press_count
    try_again_button_press_count = 0    
    
@app.route('/')
def welcome():
    session.clear()
    welcome_title = "Welcome to the Task Page"
    welcome_message = "Enter you user ID and click the button below to start the tasks."
    start_button_text = "Start Tasks"
    info_text_message = "In this testing session you will have 5 tasks that are made to test user's cognitive decision making skills."
    return render_template('welcome.html', title=welcome_title, message2=info_text_message, message=welcome_message, button_text=start_button_text, task1_url=url_for('task1'))



# Function to generate a random number between 1 and 3
def generate_random_number():
    global random_number
    random_number = random.randint(1, 3)

random_number = generate_random_number()  # Generate a random number

@app.route('/task1')
def task1():
    # Initialize points if not already set
    if 'points' not in session:
        session['points'] = 0
    # Reset button states when the page is refreshed
    for button_id in button_states:
        button_states[button_id] = False
    
    # Reset highest price and button ID
    global highest_price, highest_price_button
    highest_price = 0
    highest_price_button = None
    
    button_texts.clear()
    # Increment refresh count
    refresh_count = session.get('refresh_count', 0)
    session['refresh_count'] = refresh_count + 1

    return render_template('task1.html', refresh_count=refresh_count)

@app.route('/task2')
def task2():
    # Ensure points are initialized
    if 'points' not in session:
        session['points'] = 0
    # Reset button states when the page is refreshed
    for button_id in button_states:
        button_states[button_id] = False

    matrix1, matrix2, negative_count1, negative_count2 = create_matrices()

    return render_template('task2.html', matrix1=matrix1, matrix2=matrix2, negative_count1=negative_count1, negative_count2=negative_count2)

@app.route('/task3')
def task3():
        
    # Reset button states when the page is refreshed
    for button_id in button_states:
        button_states[button_id] = False

    matrix1, matrix2, negative_count1, negative_count2 = create_matrices()

    return render_template('task3.html', matrix1=matrix1, matrix2=matrix2, negative_count1=negative_count1, negative_count2=negative_count2)

@app.route('/task4')
def task4():
    # Reset highest price and button ID
    global highest_price, highest_price_button
    highest_price = 0
    highest_price_button = None
    
    button_texts.clear()
    # Increment refresh count
    # Check if this is the user's first visit to the page
    if 'task4_visited' not in session:
        session['refresh_count'] = 0
        session['task4_visited'] = True
    else:
        # Increment refresh count
        refresh_count = session.get('refresh_count', 0)
        session['refresh_count'] = refresh_count + 1

    return render_template('task4.html', refresh_count=session['refresh_count'])

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/create_buttons')
def create_buttons():
    task_name = request.args.get('task_name', 'default_task')
    screen_width = int(request.args.get('screen_width', 1200))
    screen_height = int(request.args.get('screen_height', 800))
    button_html = ''

    if task_name == 'task1':
        button_count = 15  # Total buttons to create (3 sets of 5 buttons)
        button_width = 100
        button_height = 50

        button_html = ''

        positions = generate_random_positions(button_count, screen_width, screen_height, button_width, button_height)
        
        button_index = 0
        for set_num in range(1, 4):
            for button_num in range(1, 6):
                button_id = f'button-{set_num}-{button_num}'
                if button_num == 1:
                    button_title = f'{set_num} Hotel'
                elif button_num == 2:
                    button_title = f'{set_num} Rating'
                elif button_num == 3:
                    button_title = f'{set_num} Price'
                elif button_num == 4:
                    button_title = f'{set_num} Pool'
                else:
                    button_title = 'Button'

                x, y = positions[button_index]
                button_index += 1

                button_html += f'''
                    <button id="{button_id}" class="random-button" style="left: {x}px; top: {y}px; width: 100px; height: 50px; background-color: lightgray; color: black; border-radius: 10px; margin: 5px; position: absolute;">{button_title}</button>
                '''
        return jsonify({'button_html': button_html})
    elif task_name == 'task2':
        button_html = '''
            <button id="clickButton5" style="width: 150px; background-color: #4CAF50; color: white; border-radius: 10px; position: fixed; top: 60%; left: 36%">Button A</button>
            <button id="clickButton6" style="width: 150px; background-color: #008CBA; color: white; border-radius: 10px; position: fixed; top: 60%; left: 52%"">Button B</button>
        '''
    elif task_name == 'task3':
        button_html = '''
            <button id="clickButton5" style="width: 150px; background-color: #4CAF50; color: white; border-radius: 10px; position: fixed; top: 60%; left: 36%">Button A</button>
            <button id="clickButton6" style="width: 150px; background-color: #008CBA; color: white; border-radius: 10px; position: fixed; top: 60%; left: 52%"">Button B</button>
        '''

    
    return button_html

@app.route('/create_buttons_task4')
def create_buttons_task2():
    button_html = create_buttons_html_task2('task4')
    return jsonify({'button_html': button_html})

def create_buttons_html_task2(task_name):
    button_html = ''
    if task_name == 'task4':
        button_count = 5  # Total buttons to create (3 sets of 5 buttons)
        screen_width = 1800  # Example screen width, adjust as needed
        screen_height = 800  # Example screen height, adjust as needed
        button_width = 100
        button_height = 50

        set_count = 3
        gap_between_sets = 50
        total_width = (set_count * button_width) + ((set_count - 1) * gap_between_sets)
        start_x = (screen_width - total_width) // 2  # Center the sets horizontally

        # Calculate the starting y positions for each stack based on screen height
        total_height = (button_count * button_height) + ((button_count - 1) * 10)  # 10px gap between buttons
        start_y = (screen_height - total_height) // 2  # Center the stacks vertically
        
        
        for set_num in range(1, set_count + 1):
            x_position = start_x + (set_num - 1) * (button_width + gap_between_sets)
            for button_num in range(1, button_count + 1):
                button_id = f'button-{set_num}-{button_num}'
                y_position = start_y + (button_num - 1) * (button_height + 10)  # Adjust y position for stacking
                if button_num == 1:
                    button_title = f'{set_num} Hotel'
                elif button_num == 2:
                    button_title = f'{set_num} Rating'
                elif button_num == 3:
                    button_title = f'{set_num} Price'
                elif button_num == 4:
                    button_title = f'{set_num} Pool'
                else:
                    button_title = 'Button'

                y = 100 + button_num * (button_height + 10)

                button_html += f'''
                    <button id="{button_id}" class="stacked-button" style="left: {x_position}px; top: {y_position}px; width: {button_width}px; height: {button_height}px; background-color: lightgray; color: black; border-radius: 10px; margin: 5px; position: absolute;">{button_title}</button>
                '''

    return button_html


# Function to find the button with the highest price
@app.route('/check_highest_price', methods=['GET'])
def check_highest_price():
    highest_price = 0
    highest_price_button = ''
    for button_id, text in button_texts.items():
        if button_id.endswith('-3'):  # Check only price buttons
            price = int(text.strip('$'))  # Extract the numeric part of the price
            if price > highest_price:
                highest_price = price
                highest_price_button = button_id
                print(highest_price)
                print(highest_price_button)
    return jsonify({'highest_price_button': highest_price_button, 'highest_price': highest_price})


# Example function to generate random hotel names
def generate_random_hotel_name():
    hotels = ['Hotel A', 'Hotel B', 'Hotel C', 'Hotel D', 'Hotel E']
    return random.choice(hotels)

# Example function to generate random hotel names
def generate_pool():
    pools = ['Yes', 'No', 'Yes with bar']
    return random.choice(pools)

# Example function to generate random numbers between 1 and 5
def generate_random_rating():
    return f"{random.randint(1, 5)} Stars"

# Example function to generate random numbers between 1 and 5
def generate_random_price():
    return random.randint(100, 2000)


@app.route('/handle_button', methods=['POST'])
def handle_button():
    data = request.json
    button_id = data.get('button_id')
    task_name = data.get('task_name', 'task1')  # Default to task1 if task_name is not provided
    click_count = data.get('click_count', 0)  # Get click count from the JSON data
    

    # Print received data for debugging
    print(f"Received data - button_id: {button_id}, task_name: {task_name}, click_count: {click_count}")

    # Update button state
    if button_id in button_states:
        button_states[button_id] = True

    
    if task_name == 'task1' and button_id.startswith('button'):
        # Check if the button already has a value
        if button_id in button_texts:
            new_button_text = button_texts[button_id]
        # Perform any logic based on the task name if needed
        else:
            new_button_text = ''

            # Example: If the task is to generate random hotel names for set 1 buttons
            if button_id.endswith('-1'):
                new_button_text = generate_random_hotel_name()
                print(new_button_text)
            # Example: If the task is to generate random numbers for set 2 buttons
            elif button_id.endswith('-2'):
                new_button_text = str(generate_random_rating())
            elif button_id.endswith('-3'):
                new_button_text = str(generate_random_price())
            elif button_id.endswith('-4'):
                new_button_text = str(generate_pool())

            # Update the button text in the dictionary
            button_texts[button_id] = new_button_text
            print(button_texts)

        # Return the new button text as a JSON response
        return jsonify({'new_button_text': new_button_text})
    
    if task_name == 'task4' and button_id.startswith('button'):
        # Check if the button already has a value
        if button_id in button_texts:
            new_button_text = button_texts[button_id]
        # Perform any logic based on the task name if needed
        else:
            new_button_text = ''

            # Example: If the task is to generate random hotel names for set 1 buttons
            if button_id.endswith('-1'):
                new_button_text = generate_random_hotel_name()
                print(new_button_text)
            # Example: If the task is to generate random numbers for set 2 buttons
            elif button_id.endswith('-2'):
                new_button_text = str(generate_random_rating())
            elif button_id.endswith('-3'):
                new_button_text = str(generate_random_price())
            elif button_id.endswith('-4'):
                new_button_text = str(generate_pool())

            # Update the button text in the dictionary
            button_texts[button_id] = new_button_text
            print(button_texts)

        # Return the new button text as a JSON response
        return jsonify({'new_button_text': new_button_text})

    print(f"Handlen randominumber {random_number}")
    find_highest_price()
    highest_price_button = highest_price_details.get('button_id')
    print('Korkein hinta on' + highest_price_button)
    task_state = get_task_state(task_name, random_number)
    
    print(click_count)
    print(task_name)
    print(button_id)
    print(task_state)

    if 'points' not in session:
        session['points'] = 0

    new_points = session['points']
    print(f"Calculated points: {new_points}")

    if task_state == 'completed':
        reset_button_press_count()
        single_button_html = create_single_button(position=60, color='orange', text='Show Next Task')  # Generate single button HTML with specified parameters
        # Render new buttons HTML directly
        new_points = 10 + new_points
        session['points'] = new_points  
        new_buttons_html = render_template_string('''
            <button id="newButton1" style="display: none; width: 150px; height: 40px; background-color: aqua; color: darkblue; border-radius: 10px; position: fixed; top: 10%; left: 80%; font-size: 16px; font-family: Verdana; transform: translate(-50%, -50%);">New Button 1</button>
            <button id="newButton2" style="display: none; width: 150px; height: 40px; background-color: aqua; color: darkblue; border-radius: 10px; position: fixed; top: 20%; left: 80%; font-size: 16px; font-family: Verdana; transform: translate(-50%, -50%);">New Button 2</button>
        ''')
        
        return jsonify({
            "command": "change_background_lightgreen",
            "task_name": task_name,
            "points": new_points,
            "single_button_html": single_button_html + new_buttons_html,
            "image":{
                "path": 'static/pallo.png',  # Add image path here
                "size": "100px",  # Add image size here
                "position": "absolute",  # Add image position here
                "top": "60px",  # Add top position here
                "left": "45%"  # Add left position here
            }
        })
    elif task_state == 'not completed' and button_id in ['clickButton4', 'clickButton5', 'clickButton6', 'clickButton7', 'clickButtonA', 'clickButtonB','clickButtonC']:
        print("mentiin tänne")
        single_button_html = create_single_button(position=60, color='orange', text='Try Again')  # Generate single button HTML with specified parameters
        new_points = new_points - 5 # Set points to 0 when the task is failed
        session['points'] = new_points
        return jsonify({
            "command": "change_background_red",
            "task_name": task_name,
            "points": new_points,
            "single_button_html": single_button_html,
            })

    return jsonify({"message": "Button clicked.", "points": new_points})

negative_count1 = 0
negative_count2 = 0

@app.route('/create_matrices')
def create_matrices():
    global negative_count1, negative_count2
    matrix1 = []
    matrix2 = []
    negative_count1 = 0  # Count of negative numbers in matrix1
    negative_count2 = 0  # Count of negative numbers in matrix2

    for _ in range(3):
        row1 = [random.randint(-9, 9) for _ in range(3)]  # Generate random numbers between 1 and 9 for matrix1
        row2 = [random.randint(-9, 9) for _ in range(3)]  # Generate random numbers between 1 and 9 for matrix2
        matrix1.append(row1)
        matrix2.append(row2)

        # Count negative numbers in each row
        negative_count1 += sum(1 for num in row1 if num < 0)
        negative_count2 += sum(1 for num in row2 if num < 0)

        
    print(negative_count1)
    print(negative_count2)
    return matrix1, matrix2, negative_count1, negative_count2

if __name__ == '__main__':
    app.run(debug=True)