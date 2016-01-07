/**
 @author David Piegza

 Implements a simple graph drawing with force-directed placement in 2D and 3D.

 It uses the force-directed-layout implemented in:
 https://github.com/davidpiegza/Graph-Visualization/blob/master/layouts/force-directed-layout.js

 Drawing is done with Three.js: http://github.com/mrdoob/three.js

 To use this drawing, include the graph-min.js file and create a SimpleGraph object:

 <!DOCTYPE html>
 <html>
 <head>
 <title>Graph Visualization</title>
 <script type="text/javascript" src="path/to/graph-min.js"></script>
 </head>
 <body onload="new Drawing.SimpleGraph({layout: '3d', showStats: true, showInfo: true})">
 </bod>
 </html>

 Parameters:
 options = {
    layout: "2d" or "3d"

    showStats: <bool>, displays FPS box
    showInfo: <bool>, displays some info on the graph and layout
              The info box is created as <div id="graph-info">, it must be
              styled and positioned with CSS.


    selection: <bool>, enables selection of nodes on mouse over (it displays some info
               when the showInfo flag is set)


    limit: <int>, maximum number of nodes

    numNodes: <int> - sets the number of nodes to create.
    numEdges: <int> - sets the maximum number of edges for a node. A node will have
              1 to numEdges edges, this is set randomly.
  }


 Feel free to contribute a new drawing!

 */

var Drawing = Drawing || {};

Drawing.NodeGraph = function(options) {
    var options = options || {};

    this.layout = options.layout || "2d";
    this.layout_options = options.graphLayout || {};
    this.show_stats = options.showStats || false;
    this.show_info = options.showInfo || false;
    this.show_labels = options.showLabels || false;
    this.selection = options.selection || false;

    this.nodes = options.nodes;
    this.edges = options.edges;


    var camera, controls, scene, renderer, interaction, geometry, object_selection;
    var stats;
    var info_text = {};
    var graph = new Graph({limit: options.limit});

    var geometries = [];

    var that = this;

    var clock = new THREE.Clock();

    init();
    createGraph();
    animate();

    function init() {

        container = document.createElement( 'div' );
        document.body.appendChild( container );

        // Three.js initialization
        renderer = new THREE.WebGLRenderer({alpha: true});
        renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.sortObjects = false;
        renderer.autoClear = false;

        scene = new THREE.Scene();

        camera = new THREE.PerspectiveCamera(40, window.innerWidth/window.innerHeight, 1, 1000000);
        camera.position.z = 5000;



        /*
         controls = new THREE.TrackballControls(camera);
         controls.rotateSpeed = 0.5;
         controls.zoomSpeed = 5.2;
         controls.panSpeed = 1;
         controls.noZoom = false;
         controls.noPan = false;
         controls.staticMoving = false;
         controls.dynamicDampingFactor = 0.3;
         controls.keys = [ 65, 83, 68 ];
         controls.addEventListener('change', render);*/


        controls = new THREE.FlyControls( camera );
        controls.movementSpeed = 3000;
        controls.domElement = container;
        controls.rollSpeed = Math.PI / 4;
        controls.autoForward = false;
        controls.dragToLook = true;

        var dirLight = new THREE.DirectionalLight( 0xffffff );
        dirLight.position.set( -1, 0, 1 ).normalize();
        scene.add( dirLight );




        // Node geometry
        geometry = new THREE.SphereGeometry(100, 32, 32  );

        var toggle_edges = function(edges)
        {
            for (var key in edges)
            {
                var line = edges[key];

                line.visible = !line.visible;

            }

        }


        // Node Selection
        object_selection = new THREE.ObjectSelection(
            {
                domElement: renderer.domElement,
                selected: function(obj) {
                    // display info
                    if(obj != null && obj.node) {
                        info_text.select = obj.node.id + " - " +obj.node.data.title;

                    } else {
                        delete info_text.select;

                    }
                },
                clicked: function(obj) {
                    console.log(obj)
                    toggle_edges(obj.node.edges);
                }
            });


        container.appendChild( renderer.domElement );

        // Stats.js
        if(that.show_stats) {
            stats = new Stats();
            stats.domElement.style.position = 'absolute';
            stats.domElement.style.top = '0px';
            document.body.appendChild( stats.domElement );
        }

        // Create info box
        if(that.show_info) {
            var info = document.createElement("div");
            var id_attr = document.createAttribute("id");
            id_attr.nodeValue = "graph-info";
            info.setAttributeNode(id_attr);
            document.body.appendChild( info );
        }
    }

    /**
     *  Creates a graph with random nodes and edges.
     *  Number of nodes and edges can be set with
     *  numNodes and numEdges.
     */
    function createGraph() {


        for (var key in that.nodes) {
            var node_data = that.nodes[key];

            var node = new Node(node_data.id);
            node.edges = []
            node.data.title = node_data.text;
            node.data.size = node_data.size;
            node.position = node_data.position;
            that.nodes[key].obj = node;





            graph.addNode(node);
            drawNode(node)
        }

        for(var key in that.edges)
        {
            var edge = that.edges[key];

            var node_1 = that.nodes[edge[0]].obj;
            var node_2 = that.nodes[edge[1]].obj;

            graph.addEdge(node_1, node_2);
            var graphic_edge = drawEdge(node_1, node_2);

            node_1.edges.push(graphic_edge);
            node_2.edges.push(graphic_edge)


        }


        info_text.nodes = "Nodes " + graph.nodes.length;
        info_text.edges = "Edges " + graph.edges.length;
    }


    /**
     *  Create a node object and add it to the scene.
     */
    function drawNode(node) {


        var draw_object = new THREE.Mesh( geometry, new THREE.MeshBasicMaterial( {  color: Math.random() * 0xffffff, opacity: 0.5 } ) );
        draw_object.node = node;

        var scale = Math.min(10, 1 + (node.data.size * 0.01));

        draw_object.scale.x = scale
        draw_object.scale.y = scale
        draw_object.scale.z = scale

        if(that.show_labels) {
            if(node.data.title != undefined) {
                var label_object = new THREE.Label(node.data.title);
            } else {
                var label_object = new THREE.Label(node.id);
            }
            node.data.label_object = label_object;
            scene.add( node.data.label_object );
        }

        draw_object.position.y = node.position.y;
        draw_object.position.x = node.position.x;
        draw_object.position.z = node.position.z;
        draw_object.id = node.id;

        node.data.draw_object = draw_object;


        scene.add( node.data.draw_object );
    }


    /**
     *  Create an edge object (line) and add it to the scene.
     */
    function drawEdge(source, target) {
        var material = new THREE.LineBasicMaterial({ color: 0xffffff, opacity: 1, linewidth: 0.5 });

        var tmp_geo = new THREE.Geometry();
        tmp_geo.vertices.push(source.data.draw_object.position);
        tmp_geo.vertices.push(target.data.draw_object.position);

        line = new THREE.Line( tmp_geo, material, THREE.LinePieces );
        line.scale.x = line.scale.y = line.scale.z = 1;
        line.originalScale = 1;

        geometries.push(tmp_geo);


        line.visible = false

        scene.add( line );

        return line
    }


    function animate() {
        requestAnimationFrame( animate );

        // controls.update();

        render();

        if(that.show_info) {
            printInfo();
        }

    }


    function render() {

        // render selection
        object_selection.render(scene, camera);
        var delta = clock.getDelta();


        // update stats
        stats.update();

        controls.update(delta);

        // render scene
        renderer.clear();
        renderer.render( scene, camera );
    }

    /**
     *  Prints info from the attribute info_text.
     */
    function printInfo(text) {
        var str = '';
        for(var index in info_text) {
            if(str != '' && info_text[index] != '') {
                str += " - ";
            }
            str += info_text[index];
        }
        document.getElementById("graph-info").innerHTML = str;
    }

    // Generate random number
    function randomFromTo(from, to) {
        return Math.floor(Math.random() * (to - from + 1) + from);
    }

    // Stop layout calculation
    this.stop_calculating = function() {
        graph.layout.stop_calculating();
    }
}