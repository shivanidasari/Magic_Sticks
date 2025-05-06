import math
import tkinter as tk
import winsound

# Shoelace formula for polygon area
def shoelace_area(coords):
    n = len(coords)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += coords[i][0] * coords[j][1]
        area -= coords[j][0] * coords[i][1]
    return abs(area) / 2

# Check if valid polygon
def is_valid_polygon(sides):
    sides = sorted(sides)
    return sum(sides[:-1]) > sides[-1]

# Generate coordinates for polygon
def generate_polygon_coords(sides):
    n = len(sides)
    coords = [(0, 0)]
    angle = 0
    for i in range(n):
        x = coords[-1][0] + sides[i] * math.cos(angle)
        y = coords[-1][1] + sides[i] * math.sin(angle)
        coords.append((x, y))
        angle += (2 * math.pi) / n
    return coords[:-1]

# Use only the user-given segments to form polygon
def get_max_area_and_shape(stick_segments):
    if not is_valid_polygon(stick_segments):
        return 0, [], []

    coords = generate_polygon_coords(stick_segments)
    area = shoelace_area(coords)
    return area, coords, stick_segments

# Scale and flip points for canvas
def transform_coords(coords, canvas_size=300, padding=20):
    if not coords:
        return []
    xs, ys = zip(*coords)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y
    scale = min((canvas_size - padding) / width if width else 1,
                (canvas_size - padding) / height if height else 1)

    transformed = []
    for x, y in coords:
        tx = (x - min_x) * scale + padding / 2
        ty = (y - min_y) * scale + padding / 2
        ty = canvas_size - ty  # flip for canvas y-axis
        transformed.append((tx, ty))
    return transformed

# Display results
def calculate_max_area():
    stick_segments = []
    try:
        n = int(segment_entry.get())
        for i in range(n):
            val = int(segment_lengths[i].get())
            if val <= 0:
                raise ValueError
            stick_segments.append(val)
    except ValueError:
        show_error("Please enter valid positive integers.")
        return

    max_area, coords, _ = get_max_area_and_shape(stick_segments)

    if not coords:
        show_error("These segments can't form a valid polygon.")
        return

    # Create output frame
    result_frame = tk.Toplevel(window)
    result_frame.title("Max Area Polygon")
    result_frame.geometry("350x400")

    result_label = tk.Label(result_frame, text=f"Max Area: {max_area:.2f}", bg="pink", fg="blue")
    result_label.pack(pady=5)

    shape_label = tk.Label(result_frame, text="Polygon Shape", fg="black", font=("Arial", 10, "bold"))
    shape_label.pack()

    canvas = tk.Canvas(result_frame, width=300, height=300, bg="white")
    canvas.pack(pady=5)

    points = transform_coords(coords)
    if len(points) >= 3:
        flat_points = [coord for pt in points for coord in pt]
        canvas.create_polygon(flat_points, outline="black", fill="lightgreen", width=2)

def show_error(message):
    error_page = tk.Toplevel(window)
    error_page.title("Error")
    tk.Label(error_page, text=message, fg="red").pack(padx=10, pady=10)

def get_max_area_button_clicked():
    winsound.Beep(2700, 500)
    calculate_max_area()

# Clear input fields and widgets
def clear_inputs():
    segment_entry.delete(0, tk.END)
    for widget in window.pack_slaves():
        if widget not in [segment_label, segment_entry, segment_lengths_button, get_max_area_button, clear_button]:
            widget.destroy()
    segment_lengths.clear()

# GUI Setup
window = tk.Tk()
window.title("Polygon Max Area Calculator")
window.geometry("400x500")
window.configure(bg='light blue')

segment_label = tk.Label(window, text="Enter number of stick segments:", bg="orange")
segment_label.pack()

segment_entry = tk.Entry(window)
segment_entry.pack()

segment_lengths = []

def create_segment_length_entries():
    winsound.Beep(2500, 500)

    # Clear old widgets
    for widget in window.pack_slaves():
        if widget not in [segment_label, segment_entry, segment_lengths_button, get_max_area_button, clear_button]:
            widget.destroy()
    segment_lengths.clear()

    try:
        num_segments = int(segment_entry.get())
        if num_segments < 3:
            show_error("At least 3 segments needed.")
            return
    except ValueError:
        show_error("Enter a valid number.")
        return

    def handle_enter(event, idx):
        if idx + 1 < len(segment_lengths):
            segment_lengths[idx + 1].focus_set()
        else:
            get_max_area_button.focus_set()

    for i in range(num_segments):
        label = tk.Label(window, text=f"Length of segment {i + 1}:", bg="yellow")
        label.pack()
        entry = tk.Entry(window)
        entry.pack()
        entry.bind("<Return>", lambda e, idx=i: handle_enter(e, idx))
        segment_lengths.append(entry)

segment_lengths_button = tk.Button(window, text="Enter segment lengths", bg="purple", fg="white", command=create_segment_length_entries)
segment_lengths_button.pack(pady=5)

get_max_area_button = tk.Button(window, text="Calculate Max Area", bg="light green", fg="brown", command=get_max_area_button_clicked)
get_max_area_button.pack(pady=5)

clear_button = tk.Button(window, text="Clear Inputs", bg="red", fg="white", command=clear_inputs)
clear_button.pack(pady=5)

winsound.Beep(2500, 500)
window.mainloop()
