Dataset **Cattle Detection and Counting in UAV Images** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/n/s/ez/Mg62vevK4XIyx9wMKqqwdxpLmK8LaSFP7cUbAeIuAW762KHqIR7EDQCNd7oXGDiIyvbq7Gon4m6zmT3pnH4lh1yeUpfXrcRA2tIrLY9V9trfelCBuFkDS8V8sXhi.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Cattle Detection and Counting in UAV Images', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [Dataset1, images(3.17GB)](http://bird.nae-lab.org/cattle/Dataset1.zip)
- [Dataset1, annotations](http://bird.nae-lab.org/cattle/dataset1_annotation.txt)
- [Dataset2, images(72.9MB)](http://bird.nae-lab.org/cattle/Dataset2.zip)
- [Dataset2, annotations](http://bird.nae-lab.org/cattle/dataset1_annotation.txt)
