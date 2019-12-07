/* This file is automatically rebuilt by the Cesium build process. */
define(['./defined-26bd4a03', './Check-da037458', './freezeObject-2d83f591', './defaultValue-f2e68450', './Math-fa6e45cb', './Cartesian2-2a723276', './defineProperties-6f7a50f2', './Transforms-65aba0a4', './RuntimeError-ad75c885', './WebGLConstants-497deb20', './ComponentDatatype-69643096', './GeometryAttribute-ed359d71', './when-ee12a2cb', './GeometryAttributes-eecc9f43', './Plane-a1a3fd52', './VertexFormat-fbb91dc7', './FrustumGeometry-93211505'], function (defined, Check, freezeObject, defaultValue, _Math, Cartesian2, defineProperties, Transforms, RuntimeError, WebGLConstants, ComponentDatatype, GeometryAttribute, when, GeometryAttributes, Plane, VertexFormat, FrustumGeometry) { 'use strict';

    function createFrustumGeometry(frustumGeometry, offset) {
            if (defined.defined(offset)) {
                frustumGeometry = FrustumGeometry.FrustumGeometry.unpack(frustumGeometry, offset);
            }
            return FrustumGeometry.FrustumGeometry.createGeometry(frustumGeometry);
        }

    return createFrustumGeometry;

});
