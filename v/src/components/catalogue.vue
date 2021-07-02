<template>
    <div id="catalogue" class="container">
        {{_path}}{{get_catalogue}}
        <button v-if="is_root" class="btn btn-warning" id="download" @click="download">导出</button>
        <div class="col-xs-12">
            <h4 class="col-xs-12">{{question_classify}}目录</h4>
            <span class="col-xs-5 col-xs-offset-7">用户:<label style="text-weight:bold;color:purple">{{account}}</label></span>
            <button @click="exit" class="btn-link slide" id="out" >退出登录</button><br>
        </div>
        <div style="height:30px" class="col-xs-12"></div>
        <ol class="col-xs-9 col-xs-offset-2">
            <li v-for="value,index in catalogue_list">
                <a class="slide" @click="question(value)">
                    {{value}}({{solve_question_count[index]}}/{{question_count[index]}})
                </a>
            </li>
        </ol>
        <div style="height:800px"></div>
    </div>
</template>
<script>
import axios from 'axios'
import Qs from 'qs'
export default {
    data(){
        return{
            account:localStorage.getItem("account"),
            question_classify:localStorage.getItem("question_classify"),
            sex:localStorage.getItem("sex"),
            catalogue_list:'',
            question_count:'',
            solve_question_count:'',
            is_root:'',
            ip:''
        }
    },
    computed:{
        _path:function(){
            localStorage.setItem('path','/catalogue')
            if(localStorage.getItem("root")){
                this.is_root=localStorage.getItem("root")
            }
            
        },
        get_catalogue:function(){
            this.axios.post('/api/acquire/catalogue/',
                            Qs.stringify({  
                                question_classify:this.question_classify,
                                sex:this.sex
                            }),
                            {headers: {'X-CSRFToken': this.getCookie('csrftoken')}}
                            ).then((res)=>{
                                if(res.data.code==200){
                                    this.catalogue_list=res.data.catalogue_list
                                    this.question_count=res.data.question_count
                                    this.solve_question_count=res.data.solve_question_count
                                    this.ip=res.data.ip
                                }else{
                                    alert('获取目录失败')
                                }
                            })
        }
    },
    methods:{
        exit:function(){
            localStorage.clear()
            alert('退出成功')
            location.reload()
        },
        question:function(catalogue){
            localStorage.setItem('catalogue',catalogue)
            this.$router.push({
                        path:'/question',
                    })
        },
        getCookie(name) {
                var value = '; ' + document.cookie;
                var parts = value.split('; ' + name + '=');
                if (parts.length === 2) return parts.pop().split(';').shift()
        },
        download:function(){
            this.axios.post('/api/user/download/',
                            Qs.stringify({  
                                question_classify:this.question_classify,
                                account:this.account
                            }),
                            {headers: {'X-CSRFToken': this.getCookie('csrftoken')}}
                            ).then((res)=>{
                                if(res.data.code==200){
                                    alert('导出成功')
                                    this.downFile()
                                }else{
                                    alert('导出失败')
                                }
                            })
        },
        downloadFile(url, options = {}){
        return new Promise((resolve, reject) => {
          // console.log(`${url} 请求数据，参数=>`, JSON.stringify(options))
          // axios.defaults.headers['content-type'] = 'application/json;charset=UTF-8'
          axios({
            method: 'post',
            url: url, // 请求地址
            data: options, // 参数
            responseType: 'blob' // 表明返回服务器返回的数据类型
          }).then(
            response => {
              // console.log("下载响应",response)
              resolve(response.data)
              let blob = new Blob([response.data], {
                type: 'application/vnd.ms-excel'
              })
              // console.log(blob)
              // let fileName = Date.parse(new Date()) + '.xlsx'
              // 切割出文件名
              let fileNameEncode = response.headers['content-disposition'].split("filename=")[1];
              // 解码
              let fileName = decodeURIComponent(fileNameEncode)
              // console.log("fileName",fileName)
              if (window.navigator.msSaveOrOpenBlob) {
                // console.log(2)
                navigator.msSaveBlob(blob, fileName)
              } else {
                // console.log(3)
                var link = document.createElement('a')
                link.href = window.URL.createObjectURL(blob)
                link.download = fileName
                link.click()
                //释放内存
                window.URL.revokeObjectURL(link.href)
              }
            },
            err => {
              reject(err)
            }
          )
        })
      },
      // 下载文件
      downFile(){
        let postUrl= "http://"+this.ip+":8000/download/file/"
        let params = {
          filename: this.question_classify+'-'+this.sex+'-'+this.account+'.docx',
        }
        let params2 = {
          filename: this.question_classify+'-'+this.sex+'-'+this.account+'.xlsx',
        }
        // console.log("下载参数",params)
        this.downloadFile(postUrl,params)
        this.downloadFile(postUrl,params2)
      },
    }
    
}
</script>

<style scoped>
    @import "../../static/css/catalogue.css"; 
</style>