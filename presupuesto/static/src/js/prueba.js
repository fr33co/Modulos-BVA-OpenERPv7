(function() {

    app = {};

    function main() {
        $("div").click(function() {
            _.each(_.range(1, 11), function(i) {
                alert('sadasaa');
            });
        });
    };
    app.main = main;

})();