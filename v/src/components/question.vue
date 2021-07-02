<template>
    <div id="question" class="container">
        {{get_question}}{{is_catalogue}}
        <h4>{{catalogue}}</h4><br>
        <button @click="save"  id="save" class="btn-small btn-success">保存</button>
        <button @click="again" id="again" class="btn-small btn-danger">重做</button>
        <div v-for="value,index in question_list">
            <div v-if="Object.prototype.toString.call(value).slice(8,-1)=='Array'">
                <div v-for="x,y in value">
                    <div v-if="y==0">
                        <span>{{x}}</span><br>
                        <div v-if="Object.prototype.toString.call(answer_list[index]).slice(8,-1)=='Array'">
                            <select  :id="question_id[index][y]" @change="change(index)" class="answer form-control">
                                <option v-for="part in answer_list[index][y]" :value="part">{{part}}</option>
                            </select><br>   
                        </div>
                    </div>
                    <div v-if="y!=0&&is_show[index]">
                        <span  v-if="x.slice(-1,x.length+1)=='+'">{{x.slice(0,-1)}}(可复选)</span>
                        <span  v-else="x.slice(-1,x.length+1)=='+'">{{x}}</span><br>
                        <div v-if="Object.prototype.toString.call(answer_list[index][y]).slice(8,-1)=='Array'">
                            <div v-if="x.slice(-1,x.length+1)=='+'">
                                <select multiple="ture" :id="question_id[index][y]"  class="answer  form-control">
                                    <option v-for="part in answer_list[index][y]" :value="part">{{part}}</option>
                                </select><br>
                            </div>
                            <div v-else="x.slice(-1,x.length+1)=='+'">
                                <select  :id="question_id[index][y]"  class="answer  form-control">
                                    <option v-for="part in answer_list[index][y]" :value="part">{{part}}</option>
                                </select><br>
                            </div>
                        </div>
                        <div v-else="Object.prototype.toString.call(answer_list[index][y]).slice(8,-1)=='Array'">
                            <input type="text"  :id="question_id[index][y]"  class="answer  form-control"><br>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else="Object.prototype.toString.call(value).slice(8,-1)=='Array'" :class="question_id[index]">
                <span  v-if="value.slice(-1,value.length+1)=='+'">{{value.slice(0,-1)}}(可复选)</span>
                <span  v-else="value.slice(-1,value.length+1)=='+'" >{{value}}</span><br>
                <input v-if="!answer_list[index]" type="text" :id="question_id[index]" class="answer  form-control"><br> 
                <div v-if="Object.prototype.toString.call(answer_list[index]).slice(8,-1)=='Array'">
                    <div v-if="value.slice(-1,value.length+1)=='+'">
                        <select multiple="ture" :id="question_id[index]"  class="answer  form-control">
                            <option v-for="part in answer_list[index]" :value="part">{{part}}</option>
                        </select><br>
                    </div>
                    <div v-if="value.slice(-1,value.length+1)!='+'&&value.slice(value.length-7,value.length-1)=='是否母乳喂养'">
                        <select  :id="question_id[index]"  class="answer  form-control" @change="mom">
                            <option v-for="part in answer_list[index]" :value="part">{{part}}</option>
                        </select><br>
                    </div>
                    <div v-if="value.slice(-1,value.length+1)!='+'&&value.slice(value.length-7,value.length-1)!='是否母乳喂养'">
                        <select  :id="question_id[index]"  class="answer  form-control">
                            <option v-for="part in answer_list[index]" :value="part">{{part}}</option>
                        </select><br>
                    </div>
                </div>
            </div>
        </div>
        <div style="height: 100px;"></div>
    </div>
</template>
<script>
import Qs from 'qs'
export default {
    data(){
        return{
            catalogue:localStorage.getItem('catalogue'),
            question_classify:localStorage.getItem("question_classify"),
            sex:localStorage.getItem("sex"),
            question_list:'',
            answer_list:'',
            question_id:'',
            answer:'',
            solve_question_answer:'',
            is_show:'',
            res_id:'',
            num:'',
            id1:'',
            id2:'',
            id3:'',
        }
    },
    
    computed:{
        is_catalogue:function(){
            if(!localStorage.getItem('catalogue')){
                this.$router.push({
                        path:localStorage.getItem("path"),
                    })
            }else{
                localStorage.setItem('path','/question')
            }
        },
        get_question:function(){
            this.axios.post('/api/acquire/question/',
                            Qs.stringify({  
                                question_classify:this.question_classify,
                                catalogue:this.catalogue,
                                sex:this.sex,
                            }),
                            {headers: {'X-CSRFToken': this.getCookie('csrftoken')}}
                            ).then((res)=>{
                                if(res.data.code==200){
                                    this.question_list=res.data.question_list
                                    this.answer_list=res.data.answer_list
                                    this.question_id=res.data.question_id
                                    this.solve_question_answer=res.data.solve_question_answer
                                    this.is_show=res.data.is_show
                                    this.res_id=res.data.res_id
                                    this.timer = setTimeout(()=>{   
                                        this.give_answer()  
                                    },100);
                                    
                                }else{
                                    alert('获取问题失败')
                                }
                            })
        }
    },
    methods:{
        mom:function(){
            if(document.getElementById(this.id1).value=='是'){
                document.getElementsByClassName(this.id3)[0].style.display='none'
                document.getElementById(this.id3).style.display='none'
                document.getElementsByClassName(this.id2)[0].style.display='block'
                document.getElementById(this.id2).style.display='block'
                document.getElementById(this.id3).value=''
            }
            if(document.getElementById(this.id1).value&&document.getElementById(this.id1).value=='否'){
                document.getElementsByClassName(this.id2)[0].style.display='none'
                document.getElementById(this.id2).style.display='none'
                document.getElementsByClassName(this.id3)[0].style.display='block'
                document.getElementById(this.id3).style.display='block'
                document.getElementById(this.id2).value=''
            }
        },
        save:function(){
            var problem=document.getElementsByTagName('span')
            for(var w=0;w<problem.length;w++){
                if(problem[w].innerHTML=='12:腰臀围比：'){
                    document.getElementById('a11').value=document.getElementById('a9').value+':'+document.getElementById('a10').value
                    document.getElementById('a11').disabled='disabled'
                }
            }
            var solvue_question=[]
            for(var i=0;i<this.res_id.length;i++){
                try {
                     if(document.getElementById(this.res_id[i]).multiple==true){
                        const options = document.getElementById(this.res_id[i]).options
                        const selectedValueArr = []
                        for (let i = 0; i < options.length; i++) {
                            // 如果该option被选中，则将它的value存入数组
                            if (options[i].selected) {
                                selectedValueArr.push(options[i].value)
                            }
                        }
                    
                        // 如果后端需要字符串形式，比如逗号分隔
                        this.answer = selectedValueArr.join('#')
                    }
                    else{
                        if(document.getElementById(this.res_id[i])){
                            this.answer=document.getElementById(this.res_id[i]).value
                        }else{
                            this.answer=''
                        }
                    }
                } 
                catch (e) {
                    if(document.getElementById(this.res_id[i])){
                            this.answer=document.getElementById(this.res_id[i]).value
                        }else{
                            this.answer=''
                        }
                }
                solvue_question.push(this.answer)
            }
            

            this.axios.post('/api/handle/solve_question/',
                            Qs.stringify({  
                                question_classify:this.question_classify,
                                catalogue:this.catalogue,
                                sex:this.sex,
                                solvue_question:JSON.stringify(solvue_question),
                            }),
                            {headers: {'X-CSRFToken': this.getCookie('csrftoken')}}
                            ).then((res)=>{
                                if(res.data.code==200){
                                    console.log(solvue_question)
                                    alert('保存成功')
                                    this.$router.replace('/catalogue')
                                }else{
                                    alert('保存失败')
                                }
                            })
            
        },
        change:function(index){
            
            if(document.getElementById(this.question_id[index][0]).value!='无'&&
                document.getElementById(this.question_id[index][0]).value&&
                document.getElementById(this.question_id[index][0]).value!='否'&&
                document.getElementById(this.question_id[index][0]).value!='养生餐'&&
                document.getElementById(this.question_id[index][0]).value!='素食者'&&
                document.getElementById(this.question_id[index][0]).value!='节食'&&
                document.getElementById(this.question_id[index][0]).value!='从不'
            ){
                this.is_show[index]=true
            }else{
                this.is_show[index]=false
                for(var i=1;i<this.question_id[index].length;i++){
                    
                    if(document.getElementById(this.question_id[index][i])){
                        document.getElementById(this.question_id[index][i]).value=''
                    }
                    
                }
            }
        },
        give_answer:function(){
            for(var x=0;x<this.question_id.length;x++){
                if(typeof(this.question_id[x])=='object'){
                    for(var y=0;y<this.question_id[x].length;y++){
                        if(document.getElementById(this.question_id[x][y])){
                            if(typeof(this.solve_question_answer[x][y])=='object'){
                                const options=document.getElementById(this.question_id[x][y]).options
                                for(var q=0;q<options.length;q++){
                                    for(var z=0;z<this.solve_question_answer[x][y].length;z++){
                                        if(options[q].value==this.solve_question_answer[x][y][z]){
                                            options[q].selected=true
                                        }
                                    }
                                }
                            }else{
                                document.getElementById(this.question_id[x][y]).value=this.solve_question_answer[x][y]
                            }
                        }
                        this.change(x)
                    }
                }else{
                    if(typeof(this.solve_question_answer[x])=='object'){
                        const options=document.getElementById(this.question_id[x]).options
                        for(var y=0;y<options.length;y++){
                            for(var xx=0;xx<this.solve_question_answer[x].length;xx++){
                                if(options[y].value==this.solve_question_answer[x][xx]){
                                    options[y].selected=true
                                }
                            }
                        }
                        
                    }else{
                        document.getElementById(this.question_id[x]).value=this.solve_question_answer[x]
                    }
                }
            }
            var problem=document.getElementsByTagName('span')
            for(var w=0;w<problem.length;w++){
                if(problem[w].innerHTML=='12:腰臀围比：'){
                    document.getElementById('a11').disabled='disabled'
                }
                if(problem[w].innerHTML.slice(problem[w].innerHTML.length-7,problem[w].innerHTML.length-1)=='是否母乳喂养'){
                    this.num=parseInt(problem[w].innerHTML.slice(0,problem[w].innerHTML.length-8))
                    if(this.num==36){
                        this.id1='a'+String(this.num+19)
                        this.id2='a'+String(this.num+20)
                        this.id3='a'+String(this.num+21)
                    }else{
                        this.id1='a'+String(this.num)
                        this.id2='a'+String(this.num+1)
                        this.id3='a'+String(this.num+2)
                    }
                    console.log(this.id1,this.id2,this.id3)
                    if(document.getElementById(this.id1).value=='是'){
                        document.getElementsByClassName(this.id3)[0].style.display='none'
                        document.getElementById(this.id3).style.display='none'
                        document.getElementById(this.id3).value=''
                    }
                    else{
                        document.getElementsByClassName(this.id2)[0].style.display='none'
                        document.getElementById(this.id2).style.display='none'
                        document.getElementById(this.id2).value=''
                    }
                    if(!document.getElementById(this.id1).value){
                        document.getElementsByClassName(this.id2)[0].style.display='none'
                        document.getElementById(this.id2).style.display='none'
                        document.getElementsByClassName(this.id3)[0].style.display='none'
                        document.getElementById(this.id3).style.display='none'
                        document.getElementById(this.id2).value=''
                        document.getElementById(this.id3).value=''
                    }
                }
                
            }
        },
        getCookie(name) {
                var value = '; ' + document.cookie;
                var parts = value.split('; ' + name + '=');
                if (parts.length === 2) return parts.pop().split(';').shift()
        },
        again:function(){
            for(var i=0;i<this.res_id.length;i++){
                if(document.getElementById(this.res_id[i])){
                    document.getElementById(this.res_id[i]).value=''
                }
                for (var key in this.is_show) {
                　　this.is_show[key]=false
                }
            }
        }
    }
}
</script>
<style scoped>
    #save{
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 999;
    }
    #again{
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 999;
    }
    .answer{
        position: relative;
        left: 24%;
        width: 50%;
    }
</style>

