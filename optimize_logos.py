from PIL import Image
import os

def optimize_logo(input_path, output_path, max_size=(200, 200), quality=85):
    """Optimize and resize logo images"""
    try:
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        # Resize maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized
        if output_path.endswith('.jpg') or output_path.endswith('.jpeg'):
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        else:
            img.save(output_path, 'PNG', optimize=True)
        
        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        print(f"✓ {input_path}")
        print(f"  Original: {original_size:,} bytes")
        print(f"  Optimized: {new_size:,} bytes")
        print(f"  Saved: {original_size - new_size:,} bytes ({100 - (new_size/original_size*100):.1f}%)\n")
        
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}\n")

# Optimize all logos
logos = [
    ('static/logokosar.jpg', 'static/logokosar.jpg'),
    ('static/logome.jpg', 'static/logome.jpg'),
    ('static/logoo.png', 'static/logoo.png'),
    ('static/logooo.png', 'static/logooo.png'),
]

print("Optimizing logos...\n")
for input_path, output_path in logos:
    if os.path.exists(input_path):
        optimize_logo(input_path, output_path, max_size=(200, 200), quality=85)

print("Done!")
