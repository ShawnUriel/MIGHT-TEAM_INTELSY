# PPE Detection System Using Deep Learning-Based Object Detection

**MIGHT TEAM — INTELSY Final Project Proposal**

---

## 1. Introduction (Problem Statement & Scope)

Workplace safety is a critical concern in construction sites, factories, and industrial environments. Workers are required to wear Personal Protective Equipment (PPE) such as hardhats, safety vests, and face masks to reduce the risk of injuries and accidents. However, monitoring PPE compliance is often done manually by supervisors, which can be inconsistent, time-consuming, and prone to human error. As a result, safety violations may go unnoticed, increasing the likelihood of workplace incidents.

Recent advances in computer vision and deep learning have enabled automated systems capable of detecting objects in images and videos. Object detection models such as YOLO (You Only Look Once) have demonstrated strong performance in real-time detection tasks. These models use convolutional neural networks (CNNs) to identify objects within an image and draw bounding boxes around them. Applying these technologies to workplace safety monitoring can help automate the detection of PPE usage and assist safety officers in identifying violations more efficiently.

This project proposes a **PPE detection system** that uses deep learning-based object detection models to identify safety equipment in worksite images. The system will detect three PPE categories: **hardhats**, **safety vests**, and **face masks**. The objective is to build a model that can automatically detect whether PPE equipment is present in images taken from workplace environments.

The scope of the project focuses on developing and evaluating an object detection model trained on a labeled PPE dataset. The model will be tested using images containing workers wearing or not wearing safety equipment.

### Success Metrics

The performance of the system will be evaluated using standard object detection metrics:

| Metric | Description |
|---|---|
| **mAP@0.5** | Mean Average Precision at IoU 0.5 — measures detection accuracy |
| **Precision** | Ratio of correct detections to total detections |
| **Recall** | Ratio of correct detections to total ground truths |
| **PR Curves** | Precision–Recall curves to visualize model performance trade-offs |
| **Latency** | Inference speed measured in milliseconds per image |

### Constraints

Several constraints may affect the implementation of the project:

- **Limited dataset size** may affect model generalization.
- **Hardware limitations** may restrict training time and model complexity.
- **Variations in lighting, camera angles, and worker positions** may reduce detection accuracy.

Despite these limitations, the project aims to demonstrate a working PPE detection prototype capable of identifying safety equipment in worksite images.

---

## 2. Related Work

Object detection using deep learning has become a widely used approach in computer vision applications. Below is a summary of related literature that informs this project.

1. **Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016).** You Only Look Once: Unified, Real-Time Object Detection. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR '16)*, 779–788. ACM. https://doi.org/10.1109/CVPR.2016.91

   The YOLO framework introduced a single-pass approach to object detection, predicting bounding boxes and class probabilities directly from images using convolutional neural networks. This enabled fast and efficient real-time detection.

2. **Bochkovskiy, A., Wang, C.-Y., & Liao, H.-Y. M. (2020).** YOLOv4: Optimal Speed and Accuracy of Object Detection. *arXiv preprint arXiv:2004.10934*.

   YOLOv4 enhanced both speed and accuracy through architectural improvements such as CSPDarknet53 backbone, SPP, and PAN, along with optimized training techniques (Mosaic augmentation, CIoU loss), making YOLO-based models suitable for real-time detection tasks in practical environments.

3. **Fang, W., Ding, L., Zhong, B., Love, P. E. D., & Luo, H. (2018).** Automated detection of workers and heavy equipment on construction sites: A convolutional neural network approach. *Advanced Engineering Informatics*, 37, 139–149. ACM. https://doi.org/10.1016/j.aei.2018.05.003

   This study proposed a computer vision-based framework for detecting personal protective equipment in construction environments using deep learning, demonstrating that automated PPE detection can significantly improve safety monitoring.

4. **Nath, N. D., Behzadan, A. H., & Paal, S. G. (2020).** Deep learning for site safety: Real-time detection of personal protective equipment. *Automation in Construction*, 112, 103085. ACM. https://doi.org/10.1016/j.autcon.2020.103085

   Developed a PPE detection system using YOLO-based models to identify safety helmets and vests in construction sites, showing that deep learning models can effectively detect safety equipment even in complex environments with multiple workers and background objects.

5. **Jocher, G., Chaurasia, A., & Qiu, J. (2023).** Ultralytics YOLOv8. https://github.com/ultralytics/ultralytics

   The YOLOv8 architecture provides a flexible, state-of-the-art, and lightweight implementation suitable for training custom object detection models on smaller datasets. It supports multiple tasks (detection, segmentation, classification) and offers built-in export to ONNX, TensorRT, and other formats for deployment.

---

## 3. Dataset Plan

The dataset used for this project will consist of labeled images containing workers wearing or not wearing PPE equipment. The images will include three main object categories: **hardhats**, **safety vests**, and **face masks**.

### Dataset Source

Possible datasets will be obtained from publicly available sources:

| Source | Description |
|---|---|
| **Roboflow PPE Dataset** | Pre-annotated PPE datasets in YOLO format from Roboflow Universe |
| **Kaggle PPE Detection Dataset** | Community-contributed labeled PPE image datasets |
| **Open Images Dataset** | Google's large-scale dataset with bounding box annotations |

These datasets contain annotated images with bounding boxes for PPE equipment, making them suitable for training object detection models.

### License

The datasets selected for this project will be publicly available and licensed for research and academic use. Only datasets with appropriate permissions or open licenses (such as **Creative Commons** or open research datasets) will be used.

### Consent and Privacy

To address privacy concerns, the project will focus only on detecting safety equipment rather than identifying individuals. The system will **not** perform facial recognition or collect personal identity data.

### Representativeness

To improve model performance, the dataset will include images with varying conditions:
- Different lighting environments (indoor, outdoor, shadowed)
- Multiple camera angles and distances
- Various worker positions and poses
- Diverse background settings (construction sites, factories, warehouses)

Using diverse images helps improve the model's ability to generalize to real-world scenarios.

---

## 4. Planned CNN Components and MVP

The core component of the proposed system is a **convolutional neural network-based object detection model**. Specifically, the project will utilize **YOLOv8** (Ultralytics), a modern object detection framework known for its speed, accuracy, and ease of use.

### Architecture Overview

YOLOv8 uses a CSPDarknet backbone with convolutional layers to extract visual features from images, followed by a Feature Pyramid Network (FPN) neck and decoupled detection heads that predict bounding boxes, objectness scores, and class probabilities simultaneously for each detected object.

```
Input Image (640×640)
    ↓
CSPDarknet Backbone (feature extraction)
    ↓
FPN + PAN Neck (multi-scale feature fusion)
    ↓
Detection Heads (bounding box + class predictions)
    ↓
Non-Maximum Suppression (NMS)
    ↓
Final Detections (boxes + labels + confidence)
```

During training, the model will be **fine-tuned** using a labeled dataset containing PPE objects. Starting from pretrained COCO weights, the model will learn to recognize patterns associated with hardhats, safety vests, and face masks.

### Minimum Viable Product (MVP)

The MVP of the project will include the following functionality:

- [x] Train a YOLOv8 object detection model using a labeled PPE dataset
- [x] Detect PPE objects (hardhats, vests, masks) in static images
- [x] Display bounding boxes and class labels for detected equipment
- [x] Report mAP@0.5, Precision, Recall, and PR curves
- [x] Measure inference latency

### Stretch Goals

If time and resources permit, additional improvements may be implemented:

- [ ] **Real-time PPE detection** using a webcam feed
- [ ] **Model pruning** to reduce model parameters and size
- [ ] **Quantization** (FP16 / INT8) to improve inference speed
- [ ] **ONNX / TensorRT export** for deployment optimization

---

## 5. Ethics Risk Register

Although automated monitoring systems can improve workplace safety, they may introduce ethical concerns. The project identifies the following top risks and mitigation strategies.

| # | Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|---|
| 1 | **Privacy Concerns** — Workers may feel that automated monitoring systems invade their privacy. | High | High | The system detects only PPE equipment and does **not** identify individuals or store personal data. Signage should inform workers of monitoring. |
| 2 | **Workplace Surveillance Misuse** — The system could be repurposed for excessive worker monitoring beyond safety purposes (e.g., productivity tracking). | High | Medium | The system should only be used for safety compliance monitoring. Usage policies and access controls must be established. Data minimization practices should be followed. |
| 3 | **Dataset Bias** — If the training dataset lacks diversity, the model may perform poorly across different demographics, environments, or equipment types. | Medium | Medium | Datasets from multiple sources will be used to ensure diverse images representing different workplace environments, lighting conditions, and worker demographics. Model performance will be evaluated across subgroups. |

### Additional Ethical Considerations

- **Consent**: Workers should be informed and consent to monitoring through clear signage.
- **Data Minimization**: Only minimum necessary data (images for inference) should be processed; no images should be stored beyond immediate analysis unless required.
- **Transparency**: The detection system's purpose and limitations should be clearly communicated to all stakeholders.

---

## 6. Team Roles & Milestones

### Team Roles

| Member | Role | Responsibilities |
|---|---|---|
| Member 1 | Project Lead / ML Engineer | Model training, hyperparameter tuning, evaluation |
| Member 2 | Data Engineer | Dataset collection, preprocessing, augmentation |
| Member 3 | Software Engineer | Detection pipeline, inference scripts, deployment |
| Member 4 | Documentation & QA | Proposal, report writing, testing, ethics review |

> *Note: Update member names based on your actual team composition.*

### Project Milestones

| Week | Milestone | Deliverable | Release Tag |
|---|---|---|---|
| 1 | Proposal & Setup | Proposal PDF, GitHub repo, project board | `v0.1` |
| 2 | Data Preparation | Downloaded & preprocessed dataset, EDA notebook | — |
| 3 | Baseline Model | Initial YOLOv8 training, preliminary mAP results | — |
| 4 | Model Optimization | Hyperparameter tuning, augmentation experiments | — |
| 5 | Evaluation & Stretch | PR curves, latency benchmarks, webcam demo (stretch) | — |
| 6 | Release Candidate | Full evaluation report, polished codebase | `v0.9` |
| 7 | Final Release | Final report, documentation, presentation | `v1.0` |

---

## References

[1] Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). You Only Look Once: Unified, Real-Time Object Detection. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR '16)*, 779–788. https://doi.org/10.1109/CVPR.2016.91

[2] Bochkovskiy, A., Wang, C.-Y., & Liao, H.-Y. M. (2020). YOLOv4: Optimal Speed and Accuracy of Object Detection. *arXiv preprint arXiv:2004.10934*.

[3] Fang, W., Ding, L., Zhong, B., Love, P. E. D., & Luo, H. (2018). Automated detection of workers and heavy equipment on construction sites: A convolutional neural network approach. *Advanced Engineering Informatics*, 37, 139–149. https://doi.org/10.1016/j.aei.2018.05.003

[4] Nath, N. D., Behzadan, A. H., & Paal, S. G. (2020). Deep learning for site safety: Real-time detection of personal protective equipment. *Automation in Construction*, 112, 103085. https://doi.org/10.1016/j.autcon.2020.103085

[5] Jocher, G., Chaurasia, A., & Qiu, J. (2023). Ultralytics YOLOv8. https://github.com/ultralytics/ultralytics
