""" Drinks Dataset Generator"""

import logging
import math
import random
import mathutils
import bpy
import zpy

log = logging.getLogger("zpy")
log.info("*******")
log.info("Simulation started.")

from pathlib import Path
out_path = str(Path(__file__).parent.absolute())
out_path = out_path.replace('drinks.blend','')  + "output_dataset/"
log.info("out_path: " + out_path)

def run():
    # Random seed results in unique behavior
    zpy.blender.set_seed()

    # Create the saver object
    saver = zpy.saver_image.ImageSaver(description="Drinks Dataset Generator", output_dir = out_path)
 
    # Add the label categories
    can_seg_color = zpy.color.random_color(output_style="frgb")
    saver.add_category(name="Can", color=can_seg_color)
    cans = ["coca_cola_can", "ocha_can_500ml"]
    
    bottle_seg_color = zpy.color.random_color(output_style="frgb")
    saver.add_category(name="Bottle", color=bottle_seg_color)
    bottles = ["koicha"]
    
    # Save the positions of objects so we can jitter them later
    zpy.objects.save_pose("Camera", "cam_pose")        
    all_objs = cans + bottles
    for obj in all_objs:     
            zpy.objects.save_pose(obj, obj + "_pose")
            zpy.objects.toggle_hidden(obj, hidden=True)
    
    n_cans = 2
    n_bottles = 1

    # Run the sim.
    for step_idx in zpy.blender.step():
        
        # Pick some random objects  
        objs = random.sample(cans, n_cans) + random.sample(bottles, n_bottles)
        
        
        log.info("Objects: " , str(objs))
        for obj in objs:
            # Make the object visible
            zpy.objects.toggle_hidden(obj, hidden=False)
    
            # Jitter object pose
            zpy.objects.jitter(
                obj,
                translate_range=((-1, 1), (-1, 1), (-0.5, 0.5)),
                rotate_range=(
                    (-math.pi, math.pi),
                    (-math.pi, math.pi),
                    (-math.pi, math.pi),
                ),
            )

        # Jitter the camera pose
        zpy.objects.jitter(
            "Camera",
            translate_range=(
                (-2, 2),
                (-2, 2),
                (-2, 2),
            ),
        )

        # Camera should be centered at one of the objects
        zpy.camera.look_at("Camera", bpy.data.objects[objs[0]].location)

        # HDRIs are like a pre-made background with lighting
        zpy.hdris.random_hdri()
  
        # Segment the objects
        for obj in objs:    
            color = zpy.color.random_color(output_style="frgb")
            zpy.objects.segment(obj, color=color, as_category=False)
            
        
        # Jitter the HSV for empty and full images
        hsv = (
            random.uniform(0.49, 0.51),  # (hue)
            random.uniform(0.95, 1.1),  # (saturation)
            random.uniform(0.75, 1.2),  # (value)
        )

        # Name for each of the output images
        rgb_image_name = zpy.files.make_rgb_image_name(step_idx)
        iseg_image_name = zpy.files.make_iseg_image_name(step_idx)
        #depth_image_name = zpy.files.make_depth_image_name(step_idx)

        # Render image
        zpy.render.render(
            rgb_path=saver.output_dir / rgb_image_name,
            iseg_path=saver.output_dir / iseg_image_name,
            #depth_path=saver.output_dir / depth_image_name,
            hsv=hsv,
        )

        # Add images to saver
        saver.add_image(
            name=rgb_image_name,
            style="default",
            output_path=saver.output_dir / rgb_image_name,
            frame=step_idx,
        )
        saver.add_image(
            name=iseg_image_name,
            style="segmentation",
            output_path=saver.output_dir / iseg_image_name,
            frame=step_idx,
        )
        #saver.add_image(
        #    name=depth_image_name,
        #    style="depth",
        #    output_path=saver.output_dir / depth_image_name,
        #    frame=step_idx,
        #)

           
        # Add annotation to segmentation image
        for obj in objs:   
            if obj in cans: 
                saver.add_annotation(
                    image=rgb_image_name,
                    seg_image=iseg_image_name,
                    seg_color= tuple(zpy.objects.verify(obj).seg.instance_color), 
                    category="Can")
            if obj in bottles:
                saver.add_annotation(
                    image=rgb_image_name,
                    seg_image=iseg_image_name,
                    seg_color= tuple(zpy.objects.verify(obj).seg.instance_color),
                    category="Bottle")
        

        # Return camera and objects to original positions
        zpy.objects.restore_pose("Camera", "cam_pose")   
        for obj in objs:    
            zpy.objects.restore_pose(obj, obj + "_pose")
            # Hide the objects  
            zpy.objects.toggle_hidden(obj, hidden=True)
                
        

    # Write out annotations
    saver.output_annotated_images()
    saver.output_meta_analysis()

    # ZUMO Annotations
    # zpy.output_zumo.OutputZUMO(saver).output_annotations()

    # COCO Annotations
    zpy.output_coco.OutputCOCO(saver).output_annotations()
    
    
    for obj in all_objs:    
            zpy.objects.toggle_hidden(obj, hidden=False)
    
    log.info("Simulation complete.")
    
    


if __name__ == "__main__":
    # Set the logger levels
    zpy.logging.set_log_levels("info")

    # Parse the gin-config text block
    zpy.blender.parse_config("config")

    # Run the sim
    run()
