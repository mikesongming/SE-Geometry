When tring to build an autonomous [site planning](https://en.wikipedia.org/wiki/Site_plan) model, I was shocked by the _backwardness_ of [sunlight analysis](https://www.level.org.nz/site-analysis/sun/) technology in the Chinese real estate design industry:

1. all available products are distributed as **close-sourced** "plugins" [用过的都知道~] in commercial desktop softwares, such as [AutoCAD](https://www.autodesk.com.cn/products/autocad/overview) and [Rhino Grasshopper](https://www.grasshopper3d.com/). Worse yet, many are **slow and not upgraded** for years.

2. no **python** package available makes it impossible to utilize DNN models, which nowadays are usually implemented on either [tensorflow](https://www.tensorflow.org/) or [pytorch](https://pytorch.org/), _and nothing else_.

The problem of sun position involves not only **solar astronomy** about space-time transformation between celestial and topocentric coordinates, but also  **convention** in specific industries. It needs great effort for a single person to comprehend related knowledge scattered in various papers and documents. Thus FSEG is initiated as:

1. a **container** of algorithms and know-how on _sun position_ in different industries
2. an easy-to-use API to relieve users from underlying astronomical and computational complexities
