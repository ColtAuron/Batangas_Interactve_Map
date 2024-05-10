import tkinter
import tkintermapview

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)

# map_widget.set_tile_server("https://tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=20)
# map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22) # google terrain, labels
# map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=r&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22) # google broad map, labels
# map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22) # google satellite, labels

map_widget.set_position(deg_x=13.7582328, deg_y=121.0726133)
map_widget.pack(fill="both", expand=True)

root_tk.mainloop()