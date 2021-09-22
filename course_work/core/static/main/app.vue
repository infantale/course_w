<script>

export default {
  name: "App",

  data() {
    return {
      outfits: [],
      likeFlag: false,
    };
  },

  methods: {
    pressLike: function(e) {
      e.preventDefault()
      const likeUrl = e.target.href
      if (likeUrl){
        vm = this
        axios.get(likeUrl)
        .then(function(response){
          vm.likeFlag = response.data.liked
          console.log(response.data.liked)
          }
        )
      }
    }
  },
  created: function () {
    const vm = this;
    axios.get('/api/outfits/?format=json')
    .then(function (response){


      vm.outfits = response.data
      vm.current_user = vm.outfits.pop()
    })

  },
}
</script>
