from flighthouse import create_json

buildings = [
    [[0,0,0],[1,0,0],[0,1,0]],
    [[1,0,0],[2,0,0],[1,1,0]]
]

vehicles = [
    [[
                    3.7568756875687574,
                    1.7634763476347635,
                    0.5
                ],
                [
                    3.7482953052422077,
                    1.7583404894659436,
                    0.5
                ],
                [
                    3.7391900527846236,
                    1.7624750242261864,
                    0.5
                ],
                [
                    3.7300044908545837,
                    1.7664279284786826,
                    0.5
                ],
                [
                    3.720743132777917,
                    1.7701998307276483,
                    0.5
                ],
                [
                    3.7114104370723764,
                    1.7737915978230743,
                    0.5
                ],
                [
                    3.7020107965368307,
                    1.7772043324747178,
                    0.5
                ],
                [
                    3.692548527517655,
                    1.7804393695701373,
                    0.5
                ],
                [
                    3.683027859459166,
                    1.7834982712880867,
                    0.5
                ],
                [
                    3.6734529248454852,
                    1.786382821017895,
                    0.5
                ],
                [
                    3.6638277496390184,
                    1.7890950161150103,
                    0.5
                ],
                [
                    3.65415624431591,
                    1.7916370595420765,
                    0.5
                ],
                [
                    3.6444421955913953,
                    1.7940113504631212,
                    0.5
                ]],
                [[
                    2.270241196582498,
                    1.5361907285817888,
                    0.5
                ],
                [
                    2.260712567269458,
                    1.5331567174719414,
                    0.5
                ],
                [
                    2.251186738381133,
                    1.5301139253347178,
                    0.5
                ],
                [
                    2.2416637343635957,
                    1.5270623037195812,
                    0.5
                ],
                [
                    2.2321435808551215,
                    1.524001800954497,
                    0.5
                ],
                [
                    2.2226263047771657,
                    1.5209323619086832,
                    0.5
                ],
                [
                    2.212950243534282,
                    1.5184077156316858,
                    0.5
                ],
                [
                    2.203280907761005,
                    1.5158574321761398,
                    0.5
                ],
                [
                    2.193618270574373,
                    1.513281885127547,
                    0.5
                ],
                [
                    2.1839623062628295,
                    1.5106814326257316,
                    0.5
                ],
                [
                    2.174312990542198,
                    1.5080564171736681,
                    0.5
                ],
                [
                    2.164670300816254,
                    1.5054071654209706,
                    0.5
                ],
                [
                    2.1550342164428264,
                    1.5027339879206552,
                    0.5
                ],
                [
                    2.145404719006395,
                    1.5000371788577518,
                    0.5
                ],
                [
                    2.135781792598174,
                    1.4973170157483113,
                    0.5
                ],
                [
                    2.126165424104732,
                    1.4945737591073212,
                    0.5
                ],
                [
                    2.1165556035062183,
                    1.4918076520840156,
                    0.5
                ],
                [
                    2.106952324185321,
                    1.4890189200630384,
                    0.5
                ],
                [
                    2.0973555832481274,
                    1.4862077702298926,
                    0.5
                ],
                [
                    2.0877653818581066,
                    1.4833743910990944,
                    0.5
                ],
                [
                    2.078181725584482,
                    1.4805189520034354,
                    0.5
                ],
                [
                    2.068604624766328,
                    1.4776416025427492,
                    0.5
                ],
                [
                    2.059034094893771,
                    1.4747424719905848,
                    0.5
                ],
                [
                    2.049470157007749,
                    1.4718216686571997,
                    0.5
                ],
                [
                    2.03991283811984,
                    1.4688792792073102,
                    0.5
                ],
                [
                    2.030362171653743,
                    1.4659153679310781,
                    0.5
                ],
                [
                    2.020826149343832,
                    1.4629046739072893,
                    0.5
                ],
                [
                    2.011304978488667,
                    1.4598473375589702,
                    0.5
                ],
                [
                    2.0017988765045946,
                    1.456743464966801,
                    0.5
                ],
                [
                    1.9923080719398087,
                    1.4535931270939628,
                    0.5
                ],
                [
                    1.98283280552434,
                    1.450396358982903,
                    0.5
                ],
                [
                    1.9733733312584802,
                    1.4471531589253153,
                    0.5
                ],
                [
                    1.9639299175421148,
                    1.4438634876071499,
                    0.5
                ],
                [
                    1.9545028483474,
                    1.4405272672310263,
                    0.5
                ],
                [
                    1.9450924244371526,
                    1.437144380619057,
                    0.5
                ],
                [
                    1.9356989646312086,
                    1.4337146702997856,
                    0.5
                ],
                [
                    1.926322807122878,
                    1.4302379375837182,
                    0.5
                ],
                [
                    1.9169643108474246,
                    1.426713941632766,
                    0.5
                ],
                [
                    1.9076238569042774,
                    1.4231423985298557,
                    0.5
                ],
                [
                    1.898301850034375,
                    1.419522980355965,
                    0.5
                ],
                [
                    1.8889987201536935,
                    1.4158553142829462,
                    0.5
                ],
                [
                    1.8797149239435733,
                    1.4121389816916732,
                    0.5
                ],
                [
                    1.870450946497937,
                    1.4083735173263203,
                    0.5
                ],
                [
                    1.8612073030268865,
                    1.4045584084969283,
                    0.5
                ],
                [
                    1.8519845406154443,
                    1.400693094343837,
                    0.5
                ],
                [
                    1.842783240035374,
                    1.396776965179062,
                    0.5
                ],
                [
                    1.8336040176070543,
                    1.3928093619212465,
                    0.5
                ],
                [
                    1.824447527107278,
                    1.3887895756424118,
                    0.5
                ],
                [
                    1.8153144617176076,
                    1.3847168472463605,
                    0.5
                ],
                [
                    1.8062055560064958,
                    1.3805903673001985,
                    0.5
                ],
                [
                    1.7971215879368143,
                    1.376409276042045,
                    0.5
                ],
                [
                    1.7880633808886666,
                    1.3721726635895206,
                    0.5
                ],
                [
                    1.7790318056854306,
                    1.3678795703750313,
                    0.5
                ],
                [
                    1.770027782608853,
                    1.363528987835134,
                    0.5
                ],
                [
                    1.7610522833867137,
                    1.3591198593823242,
                    0.5
                ],
                [
                    1.7521063331341102,
                    1.3546510816883743,
                    0.5
                ],
                [
                    1.7431910122267797,
                    1.3501215063087924,
                    0.5
                ],
                [
                    1.7343074580821145,
                    1.3455299416779938,
                    0.5
                ],
                [
                    1.7254568668206656,
                    1.3408751555043052,
                    0.5
                ],
                [
                    1.7166404947780085,
                    1.3361558775928601,
                    0.5
                ],
                [
                    1.7078596598339297,
                    1.3313708031227138,
                    0.5
                ],
                [
                    1.6991157425230399,
                    1.3265185964020227,
                    0.5
                ],
                [
                    1.6904101868882246,
                    1.3215978951218048,
                    0.5
                ],
                [
                    1.6817445010359031,
                    1.3166073151245625,
                    0.5
                ],
                [
                    1.6731202573499766,
                    1.311545455698842,
                    0.5
                ],
                [
                    1.6645390923197694,
                    1.3064109054045756,
                    0.5
                ],
                [
                    1.6560027059363027,
                    1.3012022484267964,
                    0.5
                ],
                [
                    1.647512860611063,
                    1.2959180714470289,
                    0.5
                ],
                [
                    1.6390713795721783,
                    1.2905569710124023,
                    0.5
                ],
                [
                    1.6306801446947545,
                    1.2851175613723855,
                    0.5
                ],
                [
                    1.6223410937251803,
                    1.2795984827421392,
                    0.5
                ],
                [
                    1.6140562168636354,
                    1.2739984099400194,
                    0.5
                ],
                [
                    1.6058275526749128,
                    1.2683160613349762,
                    0.5
                ],
                [
                    1.597657183305071,
                    1.2625502080277589,
                    0.5
                ],
                [
                    1.5895472289903916,
                    1.2566996831783277,
                    0.5
                ],
                [
                    1.5814998418555886,
                    1.2507633913810348,
                    0.5
                ],
                [
                    1.57174195576611,
                    1.2485762336215755,
                    0.5
                ],
                [
                    1.5620082360740999,
                    1.246283920170633,
                    0.5
                ],
                [
                    1.552300617777351,
                    1.2438834729196762,
                    0.5
                ],
                [
                    1.542621185827397,
                    1.2413717808354012,
                    0.5
                ],
                [
                    1.5329721852845892,
                    1.2387456070930731,
                    0.5
                ],
                [
                    1.5233560315674781,
                    1.2360015976745597,
                    0.5
                ],
                [
                    1.5137753207025264,
                    1.2331362915264845,
                    0.5
                ],
                [
                    1.5042328394629296,
                    1.2301461323681884,
                    0.5
                ],
                [
                    1.4947315752670183,
                    1.2270274822307905,
                    0.5
                ]]

]

j = create_json(vehicles,obstacles=buildings)
print(j)