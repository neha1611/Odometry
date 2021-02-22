window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        getOffset: function (value) {
            return '{"offset":"'+(new Date()).getTimezoneOffset()+'"}';
        }
    }
});