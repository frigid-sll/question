
<template>
  <div style="width: 70%;margin-left: 30px;margin-top: 30px;">
    <el-button class="filter-item" type="success" icon="el-icon-download" @click="downFile()">下载</el-button>
  </div>
</template>
 
<script>
  import axios from 'axios'
 
  export default {
    data() {
      return {
      }
    },
    methods: {
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
        let postUrl= "http://192.168.0.115:8000/download/file/"
        let params = {
          filename: "大江大河.xlsx",
        }
        // console.log("下载参数",params)
        this.downloadFile(postUrl,params)
      },
    }
  }
</script>
 
<style>
</style>