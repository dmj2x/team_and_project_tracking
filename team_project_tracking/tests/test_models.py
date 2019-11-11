from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import (authenticate, get_user_model)
from partial_date import PartialDate
from team_project_tracking.models import Course

class CourseTestCase(TestCase):
    def setUp(self):
        self.client = Client
        Course.objects.create(course_name="Software Engineering", course_number="CECS 550", semester="fall", year=PartialDate('2019'))

    def test_create_course(self):
        """check new course created"""
        softEng = Course.objects.get(course_name="Software Engineering")
        
        self.assertEqual(softEng.semester, "fall")
        self.assertEqual(softEng.year, PartialDate('2019'))

    # def test_community_str_property(self):
    #     gal = Course.objects.get(course_name="Galeras")
    #     self.assertEqual(str(gal), gal.course_name)

    # def test_community_get_absolute_url(self):
    #     gal = Community.objects.get(course_name="Galeras")
    #     self.assertIsNotNone(gal.get_absolute_url())

    # TODO: test get_absolute_url() status_code = 200
    # def test_course_name_in_resp(self):
    #     gal = Community.objects.get(course_name="Galeras")
    #     response = self.client.get(gal.get_absolute_url())
    #     self.assertContains(response, gal.course_name)
    # def test_population_in_resp(self):
    #     los = Community.objects.get(course_name="Los Rios")
    #     response = self.client.get(los.get_absolute_url())
    #     self.assertContains(response, los.population)


# class ProjectTestCase(TestCase):
#     def setUp(self):
#         gal = Community(course_name='Galeras')
#         gal.save()
#         san = Community(course_name="San Pedro")
#         san.save()
#         los = Community(course_name="Los Rios")
#         los.save()

#         gal_water = Project(project_name='Galeras Water Project', community=gal)
#         gal_water.save()
#         los_sani = Project(project_name='Los Rios Sanitation Project', community=los)
#         los_sani.save()

#     def test_create_project(self):
#         gal_wp = Project.objects.get(project_name='Galeras Water Project')
#         los_sp = Project.objects.get(project_name='Los Rios Sanitation Project')
#         self.assertEqual(gal_wp.project_name, 'Galeras Water Project')
#         self.assertEqual(los_sp.project_name, 'Los Rios Sanitation Project')

#     def test_project_str_property(self):
#         gal_wp = Project.objects.get(project_name='Galeras Water Project')
#         los_sp = Project.objects.get(project_name='Los Rios Sanitation Project')
#         self.assertEqual(str(gal_wp), gal_wp.project_name)
#         self.assertEqual(str(los_sp),los_sp.project_name)

#     def test_project_get_absolute_url(self):
#         gal_wp = Project.objects.get(project_name='Galeras Water Project')
#         los_sp = Project.objects.get(project_name='Los Rios Sanitation Project')
#         self.assertIsNotNone(gal_wp.get_absolute_url())
#         self.assertIsNotNone(los_sp.get_absolute_url())


# class FundingTestCase(TestCase):
#     def setUp(self):
#         # create communities
#         gal = Community(course_name='Galeras')
#         gal.save()
#         san = Community(course_name="San Pedro")
#         san.save()
#         los = Community(course_name="Los Rios")
#         los.save()

#         # create projects
#         gal_water = Project(project_name='Galeras Water Project', community=gal)
#         gal_water.save()
#         san_hyg = Project(project_name='San Pedro Hygiene Project', community=san)
#         san_hyg.save()
#         los_sani = Project(project_name='Los Rios Sanitation Project', community=los)
#         los_sani.save()

#         # create funding partners
#         luc = Funding(fund_name='Lucio')
#         luc.save()
#         dar = Funding(fund_name='Darrel')
#         dar.save()
#         lim = Funding(fund_name='Limo')
#         lim.save()

#         # create project funding
#         luc_san_fun = ProjectFunding(project=san_hyg, funding=luc, date_received='2018-11-20')
#         luc_san_fun.save()
#         dar_gal_fun = ProjectFunding(project=gal_water, funding=dar, date_received='2018-04-10')#datetime.date.today)
#         dar_gal_fun.save()
#         dar_los_fun = ProjectFunding(project=los_sani, funding=dar, date_received='2018-04-10')
#         dar_los_fun.save()

#     def test_create_funding(self):
#         luc_fun = Funding.objects.get(fund_name='Lucio')
#         dar_fun = Funding.objects.get(fund_name='Darrel')
#         self.assertEqual(luc_fun.fund_name, 'Lucio')
#         self.assertEqual(dar_fun.fund_name, 'Darrel')

#     def test_funding_str_property(self):
#         luc_fun = Funding.objects.get(fund_name='Lucio')
#         dar_fun = Funding.objects.get(fund_name='Darrel')
#         self.assertEqual(str(luc_fun), luc_fun.fund_name)
#         self.assertEqual(str(dar_fun),dar_fun.fund_name)

#     def test_funding_get_absolute_url(self):
#         luc_fun = Funding.objects.get(fund_name='Lucio')
#         dar_fun = Funding.objects.get(fund_name='Darrel')
#         lim_fun = Funding.objects.get(fund_name='Limo')
#         self.assertIsNotNone(luc_fun.get_absolute_url())
#         self.assertIsNotNone(dar_fun.get_absolute_url())
#         self.assertIsNotNone(lim_fun.get_absolute_url())

#     def test_funding_project(self):
#         luc_fun = Funding.objects.get(fund_name='Lucio')
#         dar_fun = Funding.objects.get(fund_name='Darrel')

#         san_hp = Project.objects.get(project_name='San Pedro Hygiene Project')
#         gal_wp = Project.objects.get(project_name='Galeras Water Project')
#         los_sp = Project.objects.get(project_name='Los Rios Sanitation Project')

#         luc_funding = ProjectFunding.objects.filter(funding=luc_fun)
#         dar_funding = ProjectFunding.objects.filter(funding=dar_fun)
#         self.assertEqual(list(luc_fun.project_funded.all()), [san_hp])
#         self.assertEqual(list(dar_fun.project_funded.all()), [gal_wp, los_sp])


# class ProjectStatusTestCase(TestCase):
#     def setUp(self):
#         # create communities
#         gal = Community(course_name='Galeras')
#         gal.save()
#         san = Community(course_name="San Pedro")
#         san.save()
#         los = Community(course_name="Los Rios")
#         los.save()

#         # create projects
#         gal_water = Project(project_name='Galeras Water Project', community=gal)
#         gal_water.save()
#         san_hyg = Project(project_name='San Pedro Hygiene Project', community=san)
#         san_hyg.save()
#         los_sani = Project(project_name='Los Rios Sanitation Project', community=los)
#         los_sani.save()

#         # create project status
#         User = get_user_model()
#         user = User.objects.create_superuser('foo', 'myemail@test.com', 'password')
#         gal_status = ProjectStatus(
#             project=gal_water, status='pending', status_date=str(datetime.date.today()), added_by=user)
#         gal_status.save()
#         san_status = ProjectStatus(
#             project=san_hyg, status='completed', status_date=str(datetime.date.today()), added_by=user
#         )
#         san_status.save()

#     def test_create_proj_status(self):
#         san_hp = Project.objects.get(project_name='San Pedro Hygiene Project')
#         gal_wp = Project.objects.get(project_name='Galeras Water Project')
#         los_sp = Project.objects.get(project_name='Los Rios Sanitation Project')

#         gal_stts = ProjectStatus.objects.get(project=gal_wp)
#         san_stts = ProjectStatus.objects.get(project=san_hp)
#         self.assertEqual(list(gal_wp.proj_status.all()), [gal_stts])
#         self.assertEqual(list(san_hp.proj_status.all()), [san_stts])

#     def test_proj_status_str(self):
#         san_hp = Project.objects.get(project_name='San Pedro Hygiene Project')
#         gal_wp = Project.objects.get(project_name='Galeras Water Project')

#         gal_stts = ProjectStatus.objects.get(project=gal_wp)
#         san_stts = ProjectStatus.objects.get(project=san_hp)
#         self.assertEqual(str(gal_stts), gal_stts.status)
#         self.assertEqual(str(san_stts), san_stts.status)


# class ProjectMeetingTestCase(TestCase):
#     def setUp(self):
#         # create communities
#         gal = Community(course_name='Galeras')
#         gal.save()
#         san = Community(course_name="San Pedro")
#         san.save()
#         los = Community(course_name="Los Rios")
#         los.save()

#         # create projects
#         gal_water = Project(project_name='Galeras Water Project', community=gal)
#         gal_water.save()
#         san_hyg = Project(project_name='San Pedro Hygiene Project', community=san)
#         san_hyg.save()
#         los_sani = Project(project_name='Los Rios Sanitation Project', community=los)
#         los_sani.save()

#         # create project meeting
#         gal_meeting = ProjectMeeting(project=gal_water, meeting_name='Initial Meeting', meeting_date='2019-05-30')
#         gal_meeting.save()
#         san_meeting = ProjectMeeting(project=san_hyg, meeting_name='First Meeting', meeting_date='2019-05-30')
#         san_meeting.save()
#         los_meeting = ProjectMeeting(project=los_sani, meeting_name='Second Meeting', meeting_date='2019-05-30')
#         los_meeting.save()

#     def test_create_proj_meeting(self):
#         san_hp = Project.objects.get(project_name='San Pedro Hygiene Project')
#         gal_wp = Project.objects.get(project_name='Galeras Water Project')
#         los_sp = Project.objects.get(project_name='Los Rios Sanitation Project')

#         gal_mtg = ProjectMeeting.objects.get(project=gal_wp)
#         san_mtg = ProjectMeeting.objects.get(project=san_hp)
#         los_mtg = ProjectMeeting.objects.get(project=los_sp)
#         self.assertEqual(list(gal_wp.project_meeting.all()), [gal_mtg])
#         self.assertEqual(list(san_hp.project_meeting.all()), [san_mtg])
#         self.assertEqual(list(los_sp.project_meeting.all()), [los_mtg])
