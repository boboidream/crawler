// Get accounts from https://www.newrank.cn/
let lists = $('#result_list').find('li[data-status="1"]')

let res = []
lists.map((ix,it) => {
  let id = it.getAttribute('data-account')
  if (id) res.push(id)
})
console.log(res.join(',') + ',')

