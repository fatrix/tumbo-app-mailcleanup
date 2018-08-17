def func(self):
    """
    Get filters from datastore

    We will handle the following search keys,
        (https://tools.ietf.org/html/rfc3501#section-6.4.4)
        - FROM
        - SUBJECT

        Example:

                {
                    'FROM': [
                            'info@newsletter.ch',                        ],
                    'SUBJECT': [
                            'newsletter'
                        ]
                }


        http://stackoverflow.com/questions/12809709/imap-criteria-with-multiple-ors
        https://pymotw.com/2/imaplib/
    """
    import imaplib
    M = imaplib.IMAP4_SSL(self.settings.IMAP4_SSL_SERVER)
    M.login(self.settings.USERNAME, self.settings.PASSWORD)
    inbox_data = M.select()
    self.info(self.rid, str(inbox_data))
    self.info(self.rid, str(M.list()))

    filters = {
        'FROM': [
            'news@digitecgalaxus.ch',
            'docker@info.docker.com',
            'hackers@docker.com',
            'alert@uptimerobot.com',
            'manuel@codeship.com',
            'salford@rkc.edu',
            'messages-noreply@linkedin.com',
            'support@pythonanywhere.com',
            'newsletter@info.sixt.ch',
            'gareth@morethanseven.net',
            'contact-de@happyhours-af.ch',
            'admin@pycoders.com',
            'info@meetup.com',
            'hello@visualhierarchy.co',
            'groups-noreply@linkedin.com',
            'updates@comms.packtpub.com',
            'contact-ch@enews-airfrance.com',
            'no-reply@news.admin.ch',
            'no-reply@tutum.co',
            'builds@circleci.com',
            'klm_switzerland@klm-mail.com',
            'marketing@wegroup.ch',
            'runkeeper@mg.runkeeper.com',
            'paris@contact.about.me',
            'support@codeanywhere.com',
            'newsletter@email.posterjack.com,'
            'info@e.twitter.com',
            'info@audible.de',
            'newsletter@mrlens.ch',
            'slideshare@e.slideshare.net',
            'jobmail@jobs.ch',
            'no-reply@lucidchart.com',
            'babycenter@newsletters.babycenter.com',
            'infos@jobscout24.ch',
            'info@newsletter.urech.com',
            'invitations@linkedin.com',
            'jeff@appcelerator.com',
            'lunchgate@eemms.net',
            'industry-notices@mailer.infoq.com',
            'newsletter@listserv.heise.de',
            'noreply@paperc.com',
            'noreply@statuspage.io',
            'support@btc-echo.de',
            'donovan@newsletter.ubs.com',
            'alert@uptimerobot.com',
            'noreply@newrelic.com',
            'community@contact.about.me',
            'no-reply@sns.amazonaws.com',
            'info@twitter.com',
            'support@opbeat.com',
            'alert@datadoghq.com'
        ],
        'SUBJECT': [
            'Devops Weekly #264',
            'Philip, people are looking at your LinkedIn profile',
            'Your weekly activity on about.me'
        ]
    }

    search_result = []

    for from_filter in filters['FROM']:
        typ, search_data = M.search(None, '(FROM "%s")' % from_filter)

        for num in search_data[0].split():
            typ, data_msg = M.fetch(num, '(RFC822)')
            self.info(self.rid, 'Message %s\n%s\n' %
                      (num, data_msg[0][1][:100]))
            search_result.append((num, data_msg[0][1][:400]))
            M.store(num, '+FLAGS', '\\Deleted')

    M.expunge()

    for subject_filter in filters['SUBJECT']:
        typ, search_data = M.search(None, '(SUBJECT "%s")' % subject_filter)

        for num in search_data[0].split():
            typ, data_msg = M.fetch(num, '(RFC822)')
            self.info(self.rid, 'Message %s\n%s\n' %
                      (num, data_msg[0][1][:100]))
            search_result.append((num, data_msg[0][1][:400]))
            M.store(num, '+FLAGS', '\\Deleted')

    # imap.uid('COPY', msg_uid, '<destination folder>')
    M.expunge()

    M.close()
    M.logout()
    return {'inbox_data':
            str(inbox_data),
            'search_data':
                search_result
            }
