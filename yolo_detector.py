from ultralytics import YOLO
# from pathlib import Path
from typing import Dict, List #, Union
# import cv2
# import numpy as np

class YOLOConfidenceDetector:
    def __init__(self, model_path: str = "yolo11s.pt"):
        """
        Initialize YOLO model for object detection with confidence scores.
        
        Args:
            model_path: Path to YOLO model weights
        """
        self.model = YOLO(model_path)
        self.class_names = self.model.names  # Get class names from the model
    
    def detect_confidence_dict(self, 
                            #  image_source: Union[str, Path, np.ndarray], 
                             image,
                             confidence_threshold: float = 0.25,
                             verbose: bool = False) -> Dict[str, List[float]]:
        """
        Detect objects and return dictionary with class names and confidence lists.
        
        Args:
            image_source: Path to image or numpy array
            confidence_threshold: Minimum confidence score for detections
            verbose: Whether to print detection details
            
        Returns:
            Dictionary where keys are class names and values are lists of confidence scores
        """
        # Run inference
        results = self.model.predict(
            # image_source,
            image,
            conf=confidence_threshold,
            verbose=verbose
        )
        
        # Initialize empty dictionary
        confidence_dict = {}
        
        # Process results
        for result in results:
            if result.boxes is not None and len(result.boxes) > 0:
                for box in result.boxes:
                    class_id = int(box.cls.item())
                    confidence = box.conf.item()
                    class_name = self.class_names[class_id]
                    
                    # Add confidence to the list for this class
                    if class_name not in confidence_dict:
                        confidence_dict[class_name] = []
                    confidence_dict[class_name].append(confidence)
        
        return confidence_dict

    def confidence_dict_to_sentence(self, 
                                # confidence_dict: Dict[str, List[float]], 
                                image,
                                confidence_threshold: float = 0.25,
                                verbose: bool = False,) -> str:
        """
        Convert confidence dictionary to sentence, filtering by confidence.
        
        Args:
            confidence_dict: Dictionary from detect_confidence_dict()
            min_confidence: Minimum confidence to include in sentence
            
        Returns:
            Natural language sentence describing high-confidence detections
        """
        confidence_dict = self.detect_confidence_dict(image=image, confidence_threshold=confidence_threshold, verbose=verbose)
        if not confidence_dict:
            return "I don't see any objects in this image."
        
        # Filter by confidence and count objects
        class_counts = {}
        for class_name, confidences in confidence_dict.items():
            high_confidence_count = sum(1 for conf in confidences if conf >= confidence_threshold)
            if high_confidence_count > 0:
                class_counts[class_name] = high_confidence_count
        
        if not class_counts:
            return f"I don't see any objects with confidence above {confidence_threshold} in this image."
        
        # Handle pluralization
        description_parts = []
        for class_name, count in class_counts.items():
            if count == 1:
                description_parts.append(f"{count} {class_name}")
            else:
                plural_name = self._get_plural_form(class_name)
                description_parts.append(f"{count} {plural_name}")
        
        # Format the sentence
        return self._format_sentence(description_parts)

    def _get_plural_form(self, class_name: str) -> str:
        """Get plural form of a class name."""
        irregular_plurals = {
            'person': 'people',
            'child': 'children',
            'man': 'men', 
            'woman': 'women',
            'mouse': 'mice',
            'foot': 'feet',
            'tooth': 'teeth',
            'goose': 'geese',
            'sheep': 'sheep',
            'deer': 'deer',
            'fish': 'fish',
            'species': 'species',
            'aircraft': 'aircraft',
            'analysis': 'analyses',
            'cactus': 'cacti',
            'focus': 'foci'
        }
        
        if class_name in irregular_plurals:
            return irregular_plurals[class_name]
        elif class_name.endswith('s') or class_name.endswith('x') or class_name.endswith('z') or class_name.endswith('ch') or class_name.endswith('sh'):
            return class_name + 'es'
        elif class_name.endswith('y') and not (class_name.endswith('ay') or class_name.endswith('ey') or class_name.endswith('iy') or class_name.endswith('oy') or class_name.endswith('uy')):
            return class_name[:-1] + 'ies'
        else:
            return class_name + 's'

    def _format_sentence(self, description_parts: List[str]) -> str:
        """Format parts into a natural language sentence."""
        if len(description_parts) == 1:
            return f"I see {description_parts[0]} in this image."
        elif len(description_parts) == 2:
            return f"I see {description_parts[0]} and {description_parts[1]} in this image."
        else:
            all_but_last = ', '.join(description_parts[:-1])
            return f"I see {all_but_last}, and {description_parts[-1]} in this image."


# # Initialize detector
# detector = YOLOConfidenceDetector("yolo11s.pt")

# # Example with an image path
# image_path = image.image

# # Get confidence dictionary
# confidence_dict = detector.detect_confidence_dict(image_path)

# print("Detection Results:")
# for class_name, confidences in confidence_dict.items():
#     print(f"{class_name}: {confidences}")

# Get detailed version with bounding boxes
# detailed_dict = detector.detect_confidence_dict_with_details(image_path)

# print("\nDetailed Results:")
# for class_name, details in detailed_dict.items():
#     print(f"{class_name}:")
#     print(f"  Confidences: {details['confidences']}")
#     print(f"  Detections: {len(details['confidences'])}")
#     print(f"  Class IDs: {details['class_ids']}")

# Get summary
# summary = detector.summarize_detections(confidence_dict)
# print(f"\nSummary:\n{summary}")

# Show available classes
# available_classes = detector.get_available_classes()
# print(f"\nAvailable classes: {len(available_classes)} total")