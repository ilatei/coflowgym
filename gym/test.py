import matplotlib.pyplot as plt
import numpy as np
import math

from analyse import plot_compare, validate_reward
import analyse
import benchdata

def analyse_test(isshow=True):
    result, ep_r = benchdata.exp4_benchmark_data()
    
    result, ep_r = benchdata.success_1_data()

    # result, ep_r = [39364600.0, 18354160.0, 18821576.0, 19471056.0, 25886504.0, 19555248.0, 17746832.0, 20779064.0, 23445800.0, 22203640.0, 22223008.0, 23946032.0, 21315336.0, 21533016.0, 28004440.0, 39527080.0, 21740224.0, 20862296.0, 19811776.0, 22418624.0, 23871808.0, 20651056.0, 19909232.0, 21554560.0, 22348528.0, 22020912.0, 18894592.0, 24051488.0, 18951336.0, 20581768.0, 18695920.0, 22512448.0, 21737904.0, 19686136.0, 21889552.0, 19221064.0, 19908064.0, 19745992.0, 21203024.0, 18999032.0, 19079616.0, 24856328.0, 24356808.0, 25059608.0, 24731032.0, 21121696.0, 19002568.0, 23515336.0, 21884992.0, 23190088.0, 17837000.0, 25662800.0, 31546456.0, 20813952.0, 23860864.0, 20610960.0, 20516720.0, 21301008.0, 23936840.0, 23675408.0, 21664288.0, 17366536.0, 23536112.0, 21448416.0, 23870464.0, 18104496.0, 22378984.0, 19942368.0, 23896448.0, 21044576.0, 20127088.0, 23888400.0, 20437848.0, 20364232.0, 20194104.0, 23172272.0, 20896672.0, 20455744.0, 24486592.0, 25451144.0, 19834400.0, 23381280.0, 28008768.0, 19871880.0, 22642792.0, 23546632.0, 22825872.0, 22841840.0, 18485696.0, 17398960.0, 19929720.0, 21097872.0, 20550080.0, 19238472.0, 18412304.0, 19091400.0, 18901608.0, 31318576.0, 19809440.0, 19345728.0, 18417928.0, 18655624.0, 23499864.0, 18803120.0, 29442800.0, 20174464.0, 19740608.0, 18875864.0, 18330160.0, 19634608.0, 20534704.0, 21825904.0, 21144968.0, 19704576.0, 22176912.0, 22885048.0, 18317952.0, 18973888.0, 20338720.0, 20633296.0, 21373176.0, 20855720.0, 16777416.0, 19557504.0, 23572680.0, 19879208.0, 18710896.0, 22770424.0, 17403048.0, 19196240.0, 17632328.0, 18563952.0, 23426520.0, 19481272.0, 22447400.0, 22298624.0, 20883272.0, 19782384.0, 22801648.0, 24508376.0, 21261088.0, 20575344.0, 22843352.0, 19347432.0, 20585336.0, 20573104.0, 19646472.0, 20476952.0, 22374368.0, 21665464.0, 18750000.0, 20877128.0, 22396784.0, 19136632.0, 21690864.0, 18283280.0, 19250864.0, 31678048.0, 21143336.0, 21435464.0, 20596744.0, 22155296.0, 20478992.0, 21029648.0, 21937824.0, 20028184.0, 27097232.0, 33160544.0, 21878264.0, 19594384.0, 23766632.0, 20010896.0, 24251152.0, 19991856.0, 22013424.0, 18434800.0, 23296920.0, 19786064.0, 24147096.0, 21313208.0, 20135176.0, 19661680.0, 20007336.0, 17792008.0, 20170360.0, 17834680.0, 27578288.0, 23908752.0, 18839160.0, 21055680.0, 17922008.0, 19705616.0, 17926184.0, 17976472.0, 21450888.0, 21077920.0, 22613152.0, 22061512.0, 19632168.0, 18310136.0, 19234424.0, 19433352.0, 18676824.0, 17365416.0, 19880216.0, 25164200.0, 22841944.0, 22783152.0, 19677952.0, 21278920.0, 18903624.0, 20332552.0, 18291440.0, 17114320.0, 20222152.0, 18240080.0, 24228496.0, 21391920.0, 21207344.0, 21749832.0, 21304944.0, 21690640.0, 19331784.0, 20162024.0, 18396512.0, 18531216.0, 22522960.0, 18375792.0, 17736136.0, 19484944.0, 21251184.0, 19882680.0, 18125256.0, 22762672.0, 18109256.0, 18963448.0, 25098912.0, 23104624.0, 25791984.0, 18804048.0, 19287648.0, 17623152.0, 18954896.0, 18448384.0, 18044872.0, 21601384.0, 24922776.0, 19468248.0, 26207168.0, 27116760.0, 22272072.0, 23444032.0, 20464752.0, 21443328.0, 19134040.0, 20140872.0, 19525536.0, 19135512.0, 19222048.0, 24019120.0, 19828440.0, 33819648.0, 25751864.0, 19917432.0, 18532664.0, 20360320.0, 18826808.0, 18737736.0, 20058288.0, 19268536.0, 17097040.0, 19414280.0, 17907560.0, 18941920.0, 18779008.0, 20278544.0, 23486784.0, 19773336.0, 19286288.0, 19758560.0, 18266856.0, 20886672.0, 19649760.0, 18719608.0, 19674064.0, 20133224.0, 20159552.0, 18618416.0, 19490376.0, 19327640.0, 19746032.0, 19153352.0, 19283344.0, 17143064.0, 19810768.0, 17425192.0, 21790600.0, 21869320.0, 43333632.0, 22513232.0, 19707640.0, 20597008.0, 21288280.0, 19533432.0, 20076568.0, 21136432.0, 18826928.0, 21381944.0, 19660448.0, 22519944.0, 19399104.0, 21300392.0, 19685616.0, 19141712.0, 19206768.0, 21798232.0, 22554336.0, 21863048.0, 25161112.0, 20369456.0, 20832432.0, 19391952.0, 20089736.0, 19628680.0, 18487720.0, 18765904.0, 19083288.0, 21085904.0, 23947928.0, 24283288.0, 20220656.0, 20497736.0, 19597384.0, 17851288.0, 20642776.0, 18690520.0, 23715792.0, 42007792.0, 22871184.0, 21253248.0, 19468872.0, 18595384.0, 20193512.0, 19345648.0, 20779928.0, 22709960.0, 22416192.0, 26513520.0, 19624296.0, 24674752.0, 18927824.0, 22499008.0, 20893880.0, 21798536.0, 20502000.0, 19594888.0, 18274776.0, 23902360.0, 21315568.0, 20129176.0, 18895632.0, 19033072.0, 22145472.0, 20531472.0, 21764792.0, 21599344.0, 18135752.0, 17713376.0, 28097760.0, 21604760.0, 24507424.0, 23147416.0, 22029488.0, 18860448.0, 18420968.0, 27310472.0, 21135416.0, 19329680.0, 20247320.0, 22031904.0, 21506040.0, 20360472.0, 22713352.0, 19612320.0, 20982496.0, 21308224.0, 28314504.0, 22178728.0, 20966648.0, 27012280.0, 24288600.0, 22138776.0, 19361720.0, 28822896.0, 24352920.0, 27634336.0, 23646840.0, 26481184.0, 30199344.0, 21821616.0, 26058496.0, 22145728.0, 20504920.0, 19841248.0, 30024616.0, 21899408.0, 30599552.0, 26324536.0, 22501344.0, 25990656.0, 26419992.0, 28063744.0, 26185488.0, 27281176.0, 19651872.0, 19570928.0, 20879560.0, 23559192.0, 33555056.0, 22653920.0, 36683408.0, 30436040.0, 28588152.0, 37460208.0, 29926528.0, 25346912.0, 30275416.0, 25470816.0, 27721624.0, 25356648.0, 23805936.0, 22741584.0, 25278304.0, 22156272.0, 31929576.0, 32691384.0, 27567584.0, 22593376.0, 27922936.0, 24787800.0, 19785368.0, 20300424.0, 26646064.0, 21911088.0, 22342968.0, 23835944.0, 24153600.0, 19375288.0, 24018032.0, 22823088.0, 22313208.0, 21001168.0, 22001992.0, 20346792.0, 38903672.0, 25680080.0, 20200664.0, 21247936.0, 28009696.0, 24192472.0, 21629952.0, 20743144.0, 23789712.0, 24302048.0, 22527704.0, 19196392.0, 21258864.0, 20670560.0, 28090080.0, 21756744.0, 25711952.0, 20699680.0, 20572104.0, 22234984.0, 21038424.0, 22205512.0, 31247728.0, 38229024.0, 21282072.0, 24467512.0, 32056472.0, 24667368.0, 23290072.0, 24991368.0, 22480312.0, 22038824.0, 26169376.0, 58145008.0, 22107176.0, 20169992.0, 27355968.0, 20462288.0, 22638792.0, 23379704.0, 28029672.0, 34743144.0, 30268672.0, 22268736.0, 21380624.0, 22208824.0, 33266224.0, 20308344.0, 21850912.0, 19548696.0, 24605648.0, 24648448.0, 27796688.0, 22700400.0, 41899416.0, 32325512.0, 20875112.0, 21940256.0, 24638352.0, 20394488.0, 23681016.0, 26330984.0, 20678912.0, 21745648.0, 24683928.0, 35456976.0, 29042624.0, 28092000.0, 24186792.0, 31350952.0, 27154312.0, 24194392.0, 22883040.0, 24123080.0, 24374464.0, 30479048.0, 22834464.0, 35738512.0, 23287480.0, 27142936.0, 24992840.0, 21460080.0, 27454064.0, 23770080.0, 21450592.0, 25068040.0, 18683832.0, 19286616.0, 18168200.0, 23968672.0, 22521456.0, 21487032.0, 23158112.0, 38593472.0, 25793400.0, 34111816.0, 22152032.0, 24043144.0, 20737144.0, 26056816.0, 24306368.0, 22159056.0, 49623312.0, 25905528.0, 26083864.0, 22694224.0, 45778024.0, 27579192.0, 32233752.0, 24065312.0, 20401688.0, 30438208.0, 25518456.0, 24665896.0, 21621984.0, 37568448.0, 24323320.0, 20310648.0, 22882352.0, 32837480.0, 32462608.0, 33361624.0, 23073712.0, 35634952.0, 21009936.0, 29059104.0, 47460360.0, 35939520.0, 22275672.0, 28924128.0, 24562136.0, 27566736.0, 29270736.0, 34096944.0, 46360720.0, 40406344.0, 42137208.0, 24240512.0, 30369920.0, 25329024.0, 23567872.0, 21079152.0, 19854080.0, 24212016.0, 19991736.0, 27548376.0, 23342696.0, 24689376.0, 27702264.0, 26772936.0, 21187808.0, 35071400.0, 30150952.0, 28444416.0, 40478208.0, 27118328.0, 27230040.0, 23417232.0, 24816488.0, 27070952.0, 25534168.0, 43035072.0, 40427392.0, 33677096.0, 28849664.0, 29894128.0, 28755400.0, 44500752.0, 25987864.0, 29360528.0, 30112208.0, 28499320.0, 49347552.0, 23256968.0, 49758616.0, 23748296.0, 23045920.0, 26085368.0, 25776456.0, 24618160.0, 31388712.0, 29924944.0, 22602432.0, 26504064.0, 25513584.0, 32020824.0, 28462736.0, 26971392.0, 26017888.0, 25192944.0, 24336120.0, 25072536.0, 27551880.0, 29608712.0, 46662496.0, 30499328.0, 38272144.0, 25604136.0, 25829544.0, 28652464.0, 28089704.0, 25290896.0, 30802040.0, 33014456.0, 28748408.0, 21184008.0, 27553360.0, 29539320.0, 36363568.0, 37445888.0, 35178328.0, 23082744.0, 32026248.0, 29137032.0, 34323040.0, 32397592.0, 26412288.0, 27699584.0, 37526040.0, 34213984.0, 61535672.0, 57455376.0, 29035024.0, 58408688.0, 32985712.0, 35337584.0, 25787840.0, 32855648.0, 30578896.0, 23870712.0, 23184696.0, 25730592.0, 25185720.0, 23880432.0, 24472336.0, 22096952.0, 30295488.0, 23942696.0, 30628904.0, 30009664.0, 24928848.0, 21124408.0, 27752048.0, 28170344.0, 27117976.0, 26827864.0, 22050888.0, 21902360.0, 27614656.0, 21980920.0, 22277672.0, 19905416.0, 21273064.0, 27243624.0, 21593696.0, 23031600.0, 27771856.0, 20459744.0, 25808848.0, 28426424.0, 21133592.0, 20312168.0, 32177792.0, 24922464.0, 26994872.0, 27482856.0, 42445712.0, 24817696.0, 30856296.0, 23353992.0, 26755872.0, 28452816.0, 27872552.0, 29073064.0, 25770328.0, 28546584.0, 20792744.0, 28773384.0, 25242592.0, 24878904.0, 21216560.0, 25061632.0, 29810104.0, 22398880.0, 27291376.0, 25536488.0, 25794880.0, 27009872.0, 22153904.0, 26113584.0, 28243384.0, 19316488.0, 22817896.0, 24089648.0, 28635496.0, 40317168.0, 30656528.0, 33718520.0, 30935952.0, 34428056.0, 24658048.0, 26593736.0, 19948616.0, 23903896.0, 23122792.0, 24991352.0, 24023768.0, 27594736.0, 23778456.0, 30417456.0, 23504328.0, 29536616.0, 31996480.0, 20993528.0, 21778560.0, 22358912.0, 26307256.0, 24333632.0, 19849336.0, 22865728.0, 22569728.0, 23732616.0, 22817680.0, 22215560.0, 21867680.0, 20945256.0, 23127712.0, 23345008.0, 26408208.0, 22509072.0, 24520344.0, 26777416.0, 20949632.0, 24362816.0, 22626616.0, 26042080.0, 19571408.0, 23406472.0, 28508432.0, 23734568.0, 24837200.0, 24548056.0, 23664552.0, 21519424.0, 22479728.0, 25037168.0, 32435936.0, 26201328.0, 21494120.0, 23470176.0, 23442208.0, 21438544.0, 21898080.0, 24713976.0, 24005088.0, 20658048.0, 20699400.0, 26260760.0, 23344112.0, 25107256.0, 21831496.0, 21627552.0, 21228384.0, 21157840.0, 19587544.0, 19933944.0, 20060464.0, 22019904.0, 24209160.0, 25788984.0, 21202480.0, 23086568.0, 23328696.0, 23704816.0, 29424312.0, 26323072.0, 21840352.0, 19474208.0, 23925360.0, 24139168.0, 20114896.0, 21249400.0, 25772856.0, 26951576.0, 22509504.0, 24306488.0, 22944864.0, 22302504.0, 22054376.0, 20084296.0, 23355408.0, 18209840.0, 19356760.0, 23950736.0, 22846072.0, 25163504.0, 24401496.0, 22913600.0, 28603144.0, 31271080.0, 48254152.0, 27058272.0, 29206360.0, 20938864.0, 20207016.0, 21824712.0, 29857912.0, 43391920.0, 25611904.0, 22365640.0, 28298248.0, 19295880.0, 33315960.0, 17918728.0, 21102752.0, 19008160.0, 20502880.0, 25627552.0, 27592712.0, 20905704.0, 23261000.0, 31319048.0, 23327496.0, 23103272.0, 29132648.0, 23897672.0, 25363248.0, 26340840.0, 24984784.0, 21093352.0, 21734192.0, 21899128.0, 24887208.0, 22058152.0, 23275792.0, 24048712.0, 35114232.0, 29285504.0, 30311360.0, 29109664.0, 22571272.0, 25728992.0, 20711816.0, 24530800.0, 27693000.0, 29785512.0, 29690928.0, 28405512.0, 23954712.0, 30200872.0, 25978984.0, 38421544.0, 22875864.0, 27231896.0, 22338016.0, 30769200.0, 27412448.0, 25481952.0, 28368536.0, 28659016.0, 25558168.0, 23577664.0, 26956216.0, 21283496.0, 20424568.0, 19658200.0, 23579432.0, 27465408.0, 23709744.0, 25035512.0, 35968992.0, 27097224.0, 27802816.0, 28084488.0, 34942240.0, 28341128.0, 30781024.0, 34555968.0, 24171296.0, 21165504.0, 28942040.0, 21705608.0, 22122864.0, 22843536.0, 21935064.0, 26676424.0, 21222808.0, 20906512.0, 20803888.0, 24001528.0, 28443968.0, 22739032.0, 21830040.0, 20010208.0, 20021864.0, 23838272.0, 45435888.0, 21424312.0, 20754848.0, 19436000.0, 19873768.0, 22185536.0, 22154328.0, 21843336.0, 27954680.0, 19584320.0, 28484720.0, 21366152.0, 19898888.0, 32356912.0, 20206688.0, 21727952.0, 29380672.0, 28462648.0, 27637928.0, 31375512.0, 38834600.0, 28165720.0, 30380472.0, 28966072.0, 29315712.0, 36394784.0, 22094128.0, 23968848.0, 29887864.0, 28652144.0, 26686520.0, 23077144.0, 25137432.0, 27729848.0, 23810680.0, 43719240.0, 27113968.0, 32041336.0, 33937008.0, 37456088.0, 41200576.0, 28198664.0, 28510632.0, 26747704.0, 31306536.0, 24487624.0, 22885312.0, 26796488.0, 21556672.0] , [-12887.50217089826, -2886.2170645887522, -2970.7683873944825, -3179.4392566791457, -5882.940762973315, -3167.713307994515, -2799.473919842454, -3704.82841773811, -4279.71408384114, -4275.9377756706535, -3120.118136459371, -4099.666181513587, -2984.2800949785446, -2921.184432390552, -4713.4179787191415, -8264.43570705922, -3334.1533660602017, -3396.9051558536985, -3682.8966314414824, -3177.761952928678, -5023.860133513773, -4240.745906598366, -4115.330286452669, -3901.0350851209655, -3559.48960075416, -3716.27558441685, -2952.733079101001, -4422.566507983029, -2988.8191722197744, -3716.9011808572955, -3082.3492403890755, -3332.5000318449465, -3901.844790400767, -3246.1947625375374, -3215.8342810538147, -2905.538152724828, -3346.4453347198014, -3301.8334473272125, -3776.0595645627745, -3176.398374168605, -3435.112180062846, -4405.212852512401, -4844.435874574293, -3987.531573672616, -4724.271417578201, -4007.54147338057, -3223.1219428620434, -4834.634672577872, -3766.2843402894105, -4337.664400886107, -2766.466118859638, -5284.669023282251, -7765.097419690099, -3730.767350482495, -5210.8506508939645, -3540.839641089184, -3599.4537013841596, -3646.4724830624914, -4320.840104703152, -4326.26119736126, -4465.960427289404, -2721.8481226976614, -4698.131355409987, -3878.3436655319483, -5492.92481634287, -2851.2843274839233, -4690.512279044045, -3538.73264465937, -4638.503852467264, -3936.7885044096433, -3775.347324183959, -4729.537475068574, -3477.0833445898243, -3681.7236683236147, -3385.1076892591827, -5100.148530595981, -3740.7839271078237, -3626.460500121828, -5213.259851198552, -5245.18346326571, -2930.9487012982045, -4158.358378382809, -5042.814389902427, -3390.854113276723, -3998.870781798255, -4476.52354857606, -4148.498887431048, -4268.658343644372, -3001.439830779851, -2907.1819679869836, -3268.1213943069965, -4486.582003701417, -3617.3141796092086, -3857.049822542003, -3076.507561170827, -3228.6415917233103, -3227.894410503318, -5917.617094689848, -3953.2185206000686, -3433.7212061918462, -2899.962154427788, -2947.0259850022508, -4551.227953675583, -3193.0578739736497, -5553.424747267691, -4158.817843862893, -3172.0181445359717, -3096.4395856762517, -2956.0257498293345, -3180.7175644530635, -3747.0504104118454, -4223.416534749828, -4440.864793449706, -3139.438997551776, -3536.6093071119185, -4247.796854416588, -2895.002235899397, -3225.88104023289, -4166.841961817625, -3701.435545949124, -3718.649723836572, -3437.862707190717, -2594.306541277584, -3435.0277273429565, -4637.949553122325, -3934.2746308619235, -3817.969842123888, -4260.153385878251, -2637.1413769036703, -3158.413617937864, -2964.2632464092744, -3017.881477125823, -4541.997576774625, -3263.31889399443, -4419.689208537797, -4071.6017736240724, -3765.7938287776083, -3330.7602497685116, -4849.860309623972, -5394.029050425328, -3433.5887627872576, -4110.509961501045, -4840.691677576554, -3149.6080028214287, -3454.9100721155237, -3427.624516432421, -3277.9859886186828, -3348.4188006832546, -4639.6200341106505, -4207.210335888286, -3164.9418802841533, -4178.957466293456, -4944.72903410303, -3956.0539935419715, -3687.267574250017, -2916.7310073424946, -3073.6934178312017, -7674.739824435712, -3623.8021388463344, -4179.836808259689, -4377.356627154849, -4980.386644572495, -4162.451946406309, -3347.20124624177, -3957.861928423321, -3367.028299612496, -5870.600154399065, -8354.871197216607, -3903.725475437141, -3234.1310770422815, -5065.88019511271, -4142.549254520802, -5426.638060523679, -4118.138612639366, -4711.253816113809, -3004.7832776278883, -5076.532116962684, -3357.5938269939306, -5227.8502086114395, -4247.829543868492, -3682.3352284811454, -4089.290850748244, -3290.299601368911, -2848.430225892127, -3288.78221452022, -2794.4925104429976, -5871.997387516576, -4535.837523376206, -3001.0613521133528, -3708.493364496095, -2991.51010969425, -3415.4268187265848, -3011.575896593362, -2943.7241875957748, -3980.1490396208665, -3774.0276485729346, -4353.691298130788, -3927.2931886257006, -3358.336895160794, -3050.0632221459464, -3271.159664631597, -3206.6238385595875, -3147.7087981864715, -2732.2466804622964, -3431.3248655620714, -5769.62302910801, -4423.488755283593, -4292.927289864766, -4108.331114648216, -4782.950300482525, -3197.42983008896, -3592.870470475542, -3023.3619790403595, -2718.9748017096304, -4144.122807384003, -2922.595961689866, -5553.180009500806, -3978.878444973149, -4428.046087474795, -4847.89000822789, -4572.428053961282, -4970.251703227966, -3951.5236754880634, -4170.561291355674, -2961.0621593207616, -3140.361868122351, -4375.90947395971, -3200.169999127122, -2909.689234907871, -3380.9779476890603, -3838.810056639424, -3292.8842429677634, -2959.7801819843717, -4007.486757593918, -2917.077707878295, -3047.587495421824, -5679.356323025701, -4205.064553218406, -5856.766220261195, -3235.8496386932406, -3284.2196989979143, -2863.1140263464754, -3876.1789817718677, -3010.15526465032, -2810.707349072568, -4451.806009499455, -4932.718219766401, -3954.1801365969973, -5801.659682480715, -6029.129858441788, -4285.5918479641205, -4674.597780748692, -3828.8326751642153, -4658.368457129561, -3411.021087857284, -3500.8401050188227, -3369.444623899434, -3288.3937128452976, -3257.5186320851076, -4487.621441865027, -3430.298583642315, -10057.071065084554, -5581.10975585746, -3470.503353624062, -3018.5821659742196, -3644.3863657400175, -3261.8552237466242, -3173.652607878358, -3476.5596974051537, -3441.836381427915, -2688.0088330659282, -3979.6859938220123, -3587.1298271275673, -3056.7951031839734, -3064.477339990364, -4124.630352065271, -4933.790435528622, -3377.601503787765, -3244.172774411003, -3497.403266852484, -3039.3376782301316, -3617.862634822315, -3207.583415370184, -3130.1696531751372, -3524.7401606019835, -3477.848907884487, -3662.62602799125, -3123.0261334827755, -3450.8844888163017, -3286.515722752626, -3452.713818593799, -3943.683147280568, -3342.3083591935597, -2780.6921713065994, -3344.8178031085104, -2769.4318547616085, -3886.4716512790196, -4192.534476328054, -14175.864006118163, -3920.3894427798164, -3286.069250672591, -3537.479324202551, -3865.257114727052, -3322.034053193294, -3712.9795198244747, -3847.113507422343, -3082.138427845523, -4039.1455459273166, -3932.8453315042616, -4022.7288290316296, -3982.710754259774, -4349.78664627258, -3532.9203492080774, -3265.7778605249973, -3126.832255426939, -4909.749697409605, -4061.4584108850263, -3708.632570480664, -5154.877936903741, -3179.8105202784686, -3302.3275287254487, -3348.9023287840423, -3572.840830413696, -3271.888922515791, -3018.415579890459, -3056.461103091857, -3283.6947510267087, -3722.9815716025396, -4841.194801697855, -4895.853728164645, -3368.9051789182195, -3350.194214541283, -3282.541402214829, -2870.2979759751242, -3661.933655521763, -2906.629880044365, -4675.253692200062, -14507.66380872261, -5187.277310075728, -4395.762812675029, -3154.414055117703, -3193.759445943291, -4201.502579094197, -3367.341142957373, -3651.9200911674525, -4596.926745822024, -4609.624743899193, -5193.996174446467, -3113.3876952813002, -4221.935302292557, -3222.023980550642, -4183.446412347239, -3501.225870984718, -3870.067452281555, -3333.963471451277, -3173.248004137125, -2913.5084231900983, -3901.21788179949, -4195.410553936308, -3321.7321293789505, -2992.223309750659, -3385.1569884965475, -3918.1267058569897, -4214.031581294691, -3920.0688780220594, -3957.668171662327, -2836.6993066569007, -2745.4936677897826, -6001.694552303749, -4880.40722816604, -5758.261520021126, -4113.806221809698, -4232.832658698993, -3111.9111503433196, -3074.903019569858, -6138.041824781748, -3722.595318103112, -3997.060768779077, -3383.8039177227706, -4323.737756977949, -5012.250994462421, -3314.3966982636944, -4966.9204612291105, -3917.034121979914, -3566.927538445297, -3699.6559240789984, -7368.099180455686, -3867.3212687071923, -3529.5611388275597, -5778.187300993119, -4985.542382996846, -3766.2832650148357, -3188.0091013016977, -6838.323966417196, -5488.745715995311, -6351.10421116615, -4803.341283184392, -5750.582385593716, -6368.728240621297, -3839.926371678476, -5277.980538257964, -4038.649075319818, -3442.323076292388, -3195.072476860241, -6722.502243931031, -4062.232110920269, -6683.713030420949, -5280.773635067923, -4146.508893132495, -5380.184343841277, -5051.452522626022, -5513.601663579713, -5138.341095311482, -5455.101397652886, -3504.6614313570512, -3888.8635738987164, -3229.7760621739812, -4071.135743880537, -7459.702577571539, -4171.887829765493, -7395.555239707445, -5100.264637855994, -5879.521116817362, -8464.260172516795, -5348.089158321499, -4782.012073197245, -6126.135923828493, -5351.666734769827, -6115.6780041603315, -5222.3701021254, -4828.011955383443, -4634.14029971005, -4715.6867158916275, -3945.8629816612756, -6573.036692609293, -7207.464824659037, -5219.993781927329, -4272.021446671426, -5583.407128316691, -4815.759382893182, -3283.6833385005366, -3588.4104626420303, -5978.375598084874, -4187.154788597057, -4290.827117656819, -4831.572766358687, -4845.188468111019, -3129.5145742578516, -4798.307023136617, -4285.180668747453, -4097.8783872042095, -4479.122391327701, -4772.48318593071, -3288.0423864417567, -6112.626017850664, -6012.58262690933, -3437.742697380165, -3579.3936722419644, -6480.469253552233, -4965.421856541562, -3577.0331045973594, -3777.3124762723055, -4384.527804175511, -3899.4095401958793, -4005.966718435748, -3162.2985653343353, -3086.898263812293, -2889.913353637717, -4851.673178399448, -3999.834674029602, -5201.950524390198, -3741.78633242768, -3099.6306964025034, -3904.378007645543, -3205.959382663738, -3795.9620825959373, -6815.976657786124, -11071.313165905754, -3482.0986376217934, -4011.5385745945387, -6230.144505335274, -4056.7852473795506, -4484.193187108656, -4610.142027876943, -4217.839067153914, -3993.749577164452, -3977.4823708807025, -13466.339299347643, -4308.919210712873, -3488.600718413149, -5275.221193238918, -3280.2989492158054, -3931.173625745211, -4595.322165481237, -5075.389912050033, -9250.732754161343, -6045.739358194023, -3943.5593107377917, -3730.4246225234497, -3613.359606204248, -7898.453292319282, -3808.225609137257, -3771.5731538406194, -3886.4224584674203, -5103.52407538323, -5162.183124246401, -6429.5912758095255, -4410.960257057113, -13152.500338253254, -8206.211640472076, -3380.144370052374, -3417.420785606173, -3965.3307353911578, -3274.3001361954675, -3804.85148150302, -5339.10984331912, -3574.7447601432254, -3736.140846405092, -4833.470857867192, -7961.874812546683, -6693.718970493841, -5071.066660174516, -4056.089458526776, -6467.601700126765, -5421.4293771256125, -3996.514678158832, -4369.9289189392675, -4563.849655566986, -4575.1880224098395, -6797.7331223248175, -3949.3746878297516, -11369.709275436473, -4648.526024713137, -5648.858575611685, -4852.0910099920975, -3733.4875319900693, -5307.223888412881, -4690.53242411452, -4122.469595513913, -5436.687531876674, -2996.200059019945, -2945.377784742453, -2938.9379542440956, -4434.409716043606, -4372.721415539577, -4547.012745449954, -4464.530886188043, -8337.902171028472, -4939.059070452873, -8660.20566910631, -3574.1822010644596, -3306.2288052008325, -3878.1568461724696, -5438.34960652787, -4509.177552975324, -4191.097123690507, -15283.902802181905, -3931.4762349255366, -5017.8064973236105, -4084.845011019335, -11359.485837537031, -4776.104241030874, -6286.647052418441, -4865.31864090423, -3314.944030059393, -5991.4503614379155, -5106.175267022635, -5495.946372398789, -4010.263914544104, -8180.728334920216, -5122.741338054934, -3509.3538284895844, -3883.7555191074553, -7177.668267275627, -6157.426461176366, -6109.127894540248, -3433.3942729776277, -5258.618517607154, -3493.6231937741754, -6393.858109848191, -10100.533478564043, -6900.215602685988, -3456.4100088757114, -5109.026909676849, -4468.593930817335, -5629.334721741585, -6245.55802470349, -5485.473386766741, -7331.705709941705, -6285.899613828017, -6432.648051392615, -4077.599452844716, -5227.9101194047225, -5310.85991508142, -4346.820982769689, -4006.9001603297465, -3279.0892982582986, -4660.423265752325, -3364.964323087327, -5345.986961605536, -4035.182059828631, -4441.027584715834, -4510.984252550805, -4578.609413813887, -3762.604286918606, -6171.589893884918, -5485.04238684559, -4721.176043316191, -9767.212545719673, -4705.314063527699, -4621.363648438528, -4136.621747203265, -3831.251973012556, -4917.318918809509, -4660.718247893711, -13749.557720785508, -8297.711889067246, -4982.154867446934, -3947.9687881656023, -5377.9274575206555, -4021.520119292947, -7893.56567150655, -4295.950298742509, -4695.131722933138, -4039.141806113399, -5179.38618515569, -14172.319654659757, -4152.731620207874, -13862.451729317276, -4323.198177768274, -4114.928634707696, -4958.85736829311, -5090.136857642414, -4370.037499301426, -6353.718418862335, -5487.848912054334, -3711.506998379139, -4675.762708486705, -4539.29042439893, -7055.698438290319, -5232.513123547335, -4741.158331837093, -4570.216054377256, -4160.508151788211, -4327.504180158442, -4341.641571444893, -5051.676273454313, -5691.748866577635, -13487.53733709628, -6479.357862656901, -7381.895998546179, -4579.590154918793, -4710.000925864299, -4947.972455046192, -5728.757425228968, -4776.717842598079, -7116.658501204834, -6737.847313682613, -5853.47402603672, -3203.454764096614, -4640.678076843639, -4659.993005320256, -6714.031373514534, -7399.103601018676, -5630.684145733615, -3998.5039629070275, -5459.918147188434, -6575.706643789016, -6488.795530562527, -5317.269412776665, -4638.225528580958, -5138.560315429945, -6584.7127838378865, -5034.408247719839, -9761.010207997539, -9166.023777868517, -4192.6390203114315, -16864.09542864955, -6653.145627664832, -6858.0661806491935, -5027.653316686672, -6177.031842951134, -5796.050173358801, -4189.868752805187, -4482.865759239164, -4681.762553869569, -4448.384302055172, -4287.773019557497, -4637.751390948695, -3705.7871793720087, -6383.126858983547, -4337.797153871237, -5866.455268121507, -6124.695183257008, -4528.185503929263, -3342.146047343633, -5555.610517594215, -4926.609117252379, -5644.127522414337, -5487.596884096183, -3573.52672796711, -3680.0824214079007, -5894.080655506515, -3386.0260840373485, -3707.421650576661, -3218.020095766697, -3996.067140194588, -5423.475291292078, -4101.055758963728, -4079.8828093184, -5719.427536430206, -3145.634393484557, -5066.9060440062585, -5932.7639984340685, -4026.666209308498, -3066.6434238820034, -7004.356632752147, -4453.566415480652, -5065.169221764384, -5257.30770428853, -12262.274965430319, -5391.330265607047, -6491.050671862547, -3503.766479393433, -4894.187842379506, -5752.267642202939, -5087.066802728715, -6011.226480830386, -4636.445066534123, -4852.774088732932, -3586.6877395904608, -5904.639362507786, -4877.323060646207, -4649.702471941497, -3453.7295840637494, -5680.413772855114, -6677.994692001166, -3611.6784613690556, -4724.495912541938, -5360.326507374027, -5514.182417847404, -4475.392203686728, -4647.368491962315, -4964.353480386596, -7724.19269247218, -3145.2256834036466, -3755.0697350088867, -4547.190475944632, -3996.0755063573793, -8954.591454168094, -5241.414837892678, -5735.9695224727975, -5099.786836083572, -5829.298146705018, -4079.5453473401826, -5002.668191474604, -3307.1152307206244, -4087.174771123015, -4019.873501227717, -4521.510791141551, -4048.5833628417686, -5139.933980087541, -4534.295809088012, -5687.915561357006, -3699.3079575335155, -5301.81334092929, -5573.740162131714, -3300.7663023055247, -3396.348495794608, -4152.425461701589, -5242.793206742707, -4001.583241788124, -3323.034302070988, -4308.241969854551, -4037.900738414312, -4342.038746975102, -3732.6393439847684, -3321.103588788645, -4169.823272130289, -3186.993624748224, -4715.54219252777, -3982.3305959873524, -5465.025207982766, -3500.6924943143936, -4920.918028562936, -6508.136110405065, -3566.519343613556, -4779.0754701132055, -4464.81256414305, -4649.328803511963, -3219.956695336509, -4330.708190229599, -5645.042078028606, -4479.137200449105, -4460.510614356286, -4068.587327165606, -4448.541602148858, -3650.217624706641, -3409.9712943512973, -4984.210533276737, -7324.540999120151, -5111.847701865714, -3577.2132859742364, -4329.251579107112, -3210.4027058529996, -3366.4959572031294, -3846.867783121482, -4460.544118271504, -4469.7696267434885, -3343.7279495890643, -3271.2423978065417, -5191.498034817044, -4212.891228215994, -5416.855408183959, -3196.91433499995, -3806.050958049933, -3429.85116900351, -3763.3046519219224, -3149.7394725910704, -3068.4668604093276, -3417.542588570583, -3859.4151530335607, -3662.2294413019504, -5848.4274635461115, -3524.337143842589, -4002.0256388943058, -3601.7040876947767, -3976.9120120613006, -4255.873677472677, -4705.230979935039, -3579.2182692437163, -3028.816844878447, -3578.3848318051605, -4346.421940317323, -3439.7264790768127, -3474.7226239057786, -5627.0708135794, -5590.672912032913, -4286.586842269427, -4635.904822103133, -4289.0340284183685, -3885.358839564373, -4122.33759188083, -3326.6849950108153, -4586.305456101673, -2811.7348269356116, -3215.755683739695, -4249.873054514698, -4183.794009667537, -4732.8805229753125, -4920.911878316944, -3658.8994920630553, -5427.373441713785, -6911.907800361922, -14664.228000126172, -5367.36471997856, -7301.788888752404, -3501.4977479662016, -3163.562815234052, -3576.4904414002312, -6252.9130631178605, -13339.62565233203, -4917.209204353218, -3531.7714652768364, -6891.966067405085, -3179.1121115004094, -8384.108501866504, -2741.646853257076, -3537.636435883158, -3258.127721545505, -3479.5781605721822, -4711.0621876006035, -5204.194407607576, -3458.307698996265, -4287.00845895293, -5670.309053392342, -4404.664524947824, -3745.6369260121205, -4622.872556804121, -3921.336085080953, -3834.4750438861006, -4937.034716718503, -4734.109023948071, -3594.2316577155207, -3496.4618079061956, -3569.6571623466566, -4584.7569816726755, -3767.6732587864385, -4053.9716551028605, -3772.3726484357203, -7131.121344898938, -7713.4467371021055, -6594.243403413604, -5893.268970269115, -3834.213082522973, -4665.720484939657, -3383.9750679089548, -3860.420132248398, -5223.390797079244, -6455.55414651338, -4686.512641931007, -5402.7085911944305, -4667.1651552507765, -7089.792421243058, -5176.93070482526, -12387.854090227995, -3710.216495874882, -4119.4629930774445, -3873.582490962798, -6553.002968187645, -5095.301175419335, -4684.651285940912, -6809.527637400659, -7289.326513622883, -5286.970344020275, -3492.959822343922, -5468.6906505290835, -3293.0037096283004, -3329.742013394081, -2938.4301999842687, -3775.2538138507894, -4349.928479776383, -3834.1702243918103, -5424.538275122013, -7268.726988543629, -5261.6256569267, -5075.879885785105, -4657.079710002731, -6116.133679642493, -6883.4897103645, -7858.267077510978, -8134.040011008475, -5576.427316908535, -3486.4195134350393, -7055.888189256298, -3127.451178803864, -3953.94256723989, -3787.706327938104, -3900.6284830895183, -4265.921704187346, -3831.0632211245106, -3570.40629990146, -3783.9530071859567, -4056.9739838761334, -4811.342383295891, -3493.3547926902106, -3872.5830426078933, -3016.452729177279, -3404.48068477862, -4072.6756285228257, -13067.900329430633, -4015.5274995590908, -3885.207732576459, -3124.693158638207, -2833.240318285517, -4067.0209015820965, -3956.5857225060645, -3814.3685395067446, -4774.957747941102, -3165.560980690077, -6877.176474732431, -4013.1437589128777, -3153.6218654847535, -7261.101103986267, -3324.2182622383593, -3440.165632422943, -5744.12983954006, -5016.51996273634, -7447.914143516131, -7349.929436904498, -8693.845819942562, -5767.219767742069, -5230.384594792208, -5262.837773931796, -4062.8347839998773, -6100.888447655646, -3396.436842256619, -4450.822962853176, -5856.4393497624305, -5488.593106817838, -5133.013237799082, -4290.4603147966645, -4940.346912243873, -5617.222452190658, -4814.317824191867, -12122.793390640732, -5965.508552544325, -7211.94636768743, -6743.056329559563, -6755.7294727013805, -7259.810387161522, -6214.484371211512, -6304.574737298031, -5551.488172768974, -6588.182215818345, -4738.027943349033, -3852.3845875087804, -4751.450769004206, -3075.8354639876293]




    print("Number of samples:", len(result))
    if isshow:
        # validate_reward(result, ep_r)
        plot_compare(result, ep_r, is_benchmark=True) 

        analyse.plot_smoothing(range(len(result)), result, "result")
        analyse.add_compare(is_benchmark=True)

        analyse.plot_smoothing(range(len(ep_r)), ep_r, "ep_reward")

        plt.show()
    return result, ep_r

def sentsize_analyse():
    sentsize = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9505.322576459963, 9505.322576459963, 9505.322576459963, 9505.322576459963, 19010.645152919926, 19010.645152919926, 28515.96772937989, 28515.96772937989, 28661.755146833602, 28661.755146833602, 2144678.6128822947, 2144678.6128822947, 212297436.5738683, 212297436.5738683, 249561087.99993956, 249561087.99993956, 873463808.0017198, 873463808.0017198, 2507852532.4736414, 2706374655.996888, 4005023538.072938, 5368709120.034672, 6710886399.989506, 10737418240.141117, 16106127360.678226, 16106127360.678226, 36238786561.117645, 37855922813.222496, 38923141117.14698, 53687091196.00705, 60796008569.466286, 61740154873.32862, 62416486394.990814, 80629110423.08272, 86501409005.08333, 189246996580.90283, 201325543535.78384, 248480452086.99997, 378493992788.34814, 379029815122.59106, 440411802591.9665, 542775442729.77856, 560867572972.6469, 560867572972.6469, 560867572972.6469, 562209750248.1156, 563551927523.5844, 566220766643.5763, 568905121194.5138, 570617545482.0778, 571959722757.5465, 573301900033.0153, 617868388128.9595, 680652700504.4099, 680772949619.5264, 680772949619.5264, 680935969258.2792, 680935969258.2792, 680935969258.2792, 690858665559.2069, 740315648897.62, 788778573266.4092, 790751341149.9325, 807973582760.5133, 834280283683.317, 847702677817.0414, 864773753127.4205, 890949572246.5964, 899030474835.654, 899370756569.9557, 904391501589.0104, 915296352220.1692, 923946361869.0674, 933044429245.2684, 936002142163.029, 941217290743.3174, 951757255783.5919, 958884457569.5787, 962111064558.1997, 967592827362.4146, 968909984819.0391, 974160607557.1099, 976250727027.0239, 976838351552.1116, 978198789742.8928, 991014677057.1802, 994240463485.446, 1000153905368.5172, 1017532963201.1436, 1023131617622.6857, 1029559360933.5713, 1030898837533.4852, 1041623726711.451, 1047138426550.6992, 1053672929642.272, 1058527975668.549, 1061747704269.0442, 1065005730529.8082, 1068162164992.4022, 1070854833027.1404, 1070975911490.2434, 1072398059649.215, 1073740236924.6837, 1075082414200.1525, 1076424591475.6212, 1108425327521.5815, 1140029139228.5269, 1151486053655.6414, 1165668969818.3845, 1216929235520.7595, 1270165051638.059, 1287614552544.1755, 1304851856251.1409, 1358039763763.5469, 1408147242556.953, 1410800904279.1597, 1437359657099.1953, 1476756342730.352, 1514514190011.3652, 1530979193095.6555, 1544984952679.6702, 1576379788394.9624, 1605861555096.7932, 1627144138598.8313, 1629474692037.265, 1651724352927.8772, 1673793997682.2668, 1692560653900.5237, 1705626870541.019, 1710847783197.7285, 1717654785406.3252, 1728011237197.24, 1735016593148.0442, 1741727479640.2317, 1747207425911.941, 1751233957807.2534, 1754782425578.5107, 1757365800330.298, 1793002082247.9612, 1856267147843.2883, 1906688073338.0195, 1956609757124.968, 1991899697802.1936, 2017378902901.0076, 2040660917642.3506, 2053340104802.1208, 2069228826619.596, 2082382932303.3765, 2089347905481.298, 2096090577294.029, 2100050455818.0315, 2102497167829.9338, 2104190689000.9358, 2105532866299.3733, 2106606732117.5535]

    sentsize = [e for e in sentsize if e != 0]
    import seaborn as sns 
    sns.distplot(np.log10(sentsize))
    plt.show()

def smooth_plot():
    x = np.arange(10)
    y = (x**2)
    res, _ = analyse_test()
    y = np.array(res)/1e7
    # print(y)

    DIR = "tf_log/test"
    import os 
    os
    import tensorflow as tf 
    a = tf.placeholder(dtype=tf.float32, shape=[])
    tf.summary.scalar("a", a)
    merged = tf.summary.merge_all()
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        summary = sess.run(init)
        writer = tf.summary.FileWriter(DIR, sess.graph)
        for i in range(y.shape[0]):
            s = sess.run(merged, feed_dict={a:y[i]})
            writer.add_summary(s, i)
    
def f():
    import analyse
    file = "doc/fair.txt"
    coflows = analyse.dark_analyse(file)
    print(sum(coflows))

if __name__ == "__main__":
    pass
    analyse_test()
    # sentsize_analyse()
    f()
    # smooth_plot()