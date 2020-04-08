function vtkTrakoReader() {
  
  this.decoderModule = DracoDecoderModule();
  this.decoder = new this.decoderModule.Decoder();

};

vtkTrakoReader.read = function(file, callback) {

  var xhr = new XMLHttpRequest();
  
  xhr.open('GET', file);  
  xhr.responseType = 'json';

  xhr.onload = function(r) {

    gltf = r.target.response;

    var r = new vtkTrakoReader();
    polydata = r.parse(gltf);

    callback(polydata);

  };

  xhr.send();

};


vtkTrakoReader.gltfType_to_vtkNumberOfComponents = {
  
  'SCALAR': 1,
  'VEC2': 2,
  'VEC3': 3,
  'VEC4': 4

};

vtkTrakoReader.gltfComponentType_to_size = {

  5123: 2,
  5125: 4,
  5126: 4

};

vtkTrakoReader.prototype.parse = function() {

  var polydata = vtk.Common.DataModel.vtkPolyData.newInstance();

  attributes = gltf.meshes[0].primitives[0].attributes;

  if ('properties' in gltf.meshes[0].primitives[0].extras) {
    properties = gltf.meshes[0].primitives[0].extras['properties'];
  }
  else {
    properties = {};
  }

  points = this.decode(this.decoderModule, this.decoder, gltf, attributes.POSITION);
  polydata.getPoints().setData(points, 3);

  indices = this.decode(this.decoderModule, this.decoder, gltf, gltf.meshes[0].primitives[0].indices);
  polydata.getLines().setData(indices);

  // scalars
  for (a in attributes) {

    if (a[0] == '_') {

      // we only do custom attributes now
      points = this.decode(this.decoderModule, this.decoder, gltf, attributes[a]);

      accessor = gltf.accessors[attributes[a]];

      if (accessor.type in vtkTrakoReader.gltfType_to_vtkNumberOfComponents) {
        noCmpts = vtkTrakoReader.gltfType_to_vtkNumberOfComponents[accessor.type];
      } else {
        noCmpts = accessor.type;
      }

      //
      var vtkArr = vtk.Common.Core.vtkDataArray.newInstance({
        numberOfComponents: noCmpts,
        values: points
      })
      vtkArr.setName(a);

      polydata.getPointData().addArray(vtkArr);

    }

  }

  // properties
  for (p in properties) {

    points = this.decode(this.decoderModule, this.decoder, gltf, properties[p]);

    accessor = gltf.accessors[properties[p]];

    if (accessor.type in vtkTrakoReader.gltfType_to_vtkNumberOfComponents) {
      noCmpts = vtkTrakoReader.gltfType_to_vtkNumberOfComponents[accessor.type];
    } else {
      noCmpts = accessor.type;
    }

    //
    var vtkArr = vtk.Common.Core.vtkDataArray.newInstance({
      numberOfComponents: noCmpts,
      values: points
    })
    vtkArr.setName(p);

    polydata.getCellData().addArray(vtkArr);

  }

  return polydata;

};

vtkTrakoReader.prototype.decode = function(decoderModule, decoder, gltf, which) {

  accessor = gltf.accessors[which];

  bufferview = accessor.bufferView;
  data = gltf.buffers[gltf.bufferViews[bufferview].buffer];
  
  magic = 'data:application/octet-stream;base64,'
  bytes = atob(data.uri.substring(magic.length))

  if (bytes.substring(0,5) != 'DRACO') {
    console.log('Did not find Draco compressed data..');
    return gltf;
  }


  var rawLength = bytes.length;
  // from: https://gist.github.com/borismus/1032746
  var array = new Uint8Array(new ArrayBuffer(rawLength));

  for(i = 0; i < rawLength; i++) {
    array[i] = bytes.charCodeAt(i);
  }

  var buffer = new decoderModule.DecoderBuffer();
  buffer.Init(array, rawLength);


  var pointcloud = new decoderModule.PointCloud();
  decoder.DecodeBufferToPointCloud(buffer, pointcloud);

  var attr = decoder.GetAttribute(pointcloud, 0)
  var num_points = pointcloud.num_points();

  var itemSize = vtkTrakoReader.gltfType_to_vtkNumberOfComponents[accessor.type];
  var elementBytes = vtkTrakoReader.gltfComponentType_to_size[accessor.componentType];


  array = new Float32Array(num_points*itemSize);
  var points = new decoderModule.DracoFloat32Array()
  decoder.GetAttributeFloatForAllPoints(pointcloud, attr, points)

  for (var i=0; i< num_points*itemSize; i++) {

    array[i] = points.GetValue(i);

  }
  
  if (elementBytes == 2) {

    // we need to process the indicies to be ready for rendering

    var indices = [];
    var pointer = 0;
    for (var p in array) {
      
      var length = Math.round(array[p]);

      indices.push(length);

      for(var i=pointer;i<pointer+length;i++) {
        indices.push(Math.round(i));
      }

      pointer = pointer + length

    }

    array = new Uint16Array(indices);

  }

  return array;

};
