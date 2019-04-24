Vue.use(Buefy.default, {
  defaultIconPack: 'io'
});

var searchMixin = ({
  delimiters:['<%', '%>'],
  data: function() {
    return {
      sort: '',
      search: {
        keyword: '',
        priority: '',
        status: ''
        }
    }
  },
  methods: {
  runSearch: function() {
          let destination = this.searchApi;
          let properties = this.search;
          if (this.search.category !== '') {
                for (var value in properties) {
                  if (properties[value] =! '' && properties[value]) {
                      console.log(properties[value])
                      destination += '&' + value + '=' + properties[value]
                  }
              }
              console.log(destination);
              location.replace(destination)
            }
          else {
              alert('Please select a category')
              console.log('Select category');
          }
      },
    },
    beforeMount() {
        let url_string = window.location.href;
        let url = new URL(url_string);
        let properties = this.search;
        for (var value in properties) {
            if (url.searchParams.has(value)) {
                properties[value] = url.searchParams.get(value);
            }
        }
    }
  });

var actionMixin = ({
    delimiters:['<%', '%>'],
    data: {
      actionAPI: '/api/v1/',
    },
    methods: {
        updateDocument: function(a, i, d) {
        request.post(this.actionAPI)
          .send({ action: a, id: i, data: d })
          .set('X-CSRFToken', csrf_token)
          .set('accept', 'json')
          .then(res => {
              console.log(res);
              if (res.body.destination)
                  location.replace(res.body.destination);
              else if (res.statusText == 'OK')
                  location.reload();
          })
          .catch(err => {
            console.log(err)
          });
      },
    }
});
