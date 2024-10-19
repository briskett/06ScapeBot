import os
import xml.etree.ElementTree as ET
import cv2


def parse_voc_annotation(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    objects = []
    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        objects.append((xmin, ymin, xmax, ymax))
    return objects


def create_positives_file(annotation_dir, images_dir, output_file):
    with open(output_file, 'w') as f:
        for xml_file in os.listdir(annotation_dir):
            if xml_file.endswith('.xml'):
                xml_path = os.path.join(annotation_dir, xml_file)
                print(f"Processing {xml_path}")
                objects = parse_voc_annotation(xml_path)
                if objects:
                    # Get the corresponding image filename by replacing .xml with .jpg
                    base_name = os.path.splitext(xml_file)[0] + '.jpg'
                    image_path = os.path.join(images_dir, base_name)
                    print(f"Looking for image {image_path}")
                    if os.path.exists(image_path):
                        # Write line for the image with object count and bounding boxes
                        f.write(f"{image_path} {len(objects)}")
                        for obj in objects:
                            x = obj[0]
                            y = obj[1]
                            width = obj[2] - obj[0]
                            height = obj[3] - obj[1]
                            f.write(f" {x} {y} {width} {height}")
                        f.write("\n")
                        print(f"Wrote to positives.txt: {image_path} {len(objects)} objects")
                    else:
                        print(f"Image not found: {image_path}")
                else:
                    print(f"No objects found in {xml_path}")


def draw_bounding_boxes_from_pos(pos_file):
    with open(pos_file, 'r') as file:
        for line in file:
            # Split the line into components
            components = line.strip().split(' ')

            # Extract the image path and number of boxes
            image_path = components[0]
            num_boxes = int(components[1])

            # Load the image
            image = cv2.imread(image_path)

            # Draw bounding boxes for each object
            for i in range(num_boxes):
                # Extract bounding box coordinates
                x, y, width, height = map(int, components[i * 4 + 2 : i * 4 + 6])

                # Draw bounding box rectangle
                cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

            # Display the image with bounding boxes
            cv2.imshow('Image with Bounding Boxes', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


# Example usage

images_dir = '../farmer/valid/'  # Directory containing your images
output_file = 'pos.txt'
annotations_dir = '../farmer/valid'
pos_txt_file = 'pos.txt'

#create_positives_file(annotations_dir, images_dir, output_file)
draw_bounding_boxes_from_pos(pos_txt_file)


